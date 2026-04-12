import os
from openai import OpenAI
import pandas as pd
import json
import re
import time
from base_conhecimento import BASE_CONHECIMENTO, montar_prompt
from classificador_bert import classificar_mensagem

# ── CONFIGURAÇÃO ──────────────────────────────────────────────────────────────

_client_padrao = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

ARQUIVO_ENTRADA  = "BrScamsFacebook.xlsx"
ARQUIVO_SAIDA    = "dataset_teste_rag.xlsx"
N_POR_GRUPO      = 5           # exemplos por combinação (Categoria x Dataset)
BACKUP_A_CADA    = 5           # salva backup parcial a cada N linhas
MODEL            = "gpt-4o"    # troque para o modelo que preferir


# ── SANITIZAÇÃO DE TEXTO ─────────────────────────────────────────────────────
# Remove caracteres de controle ilegais para o formato XML/XLSX (openpyxl).
# Mantém tabulação (\x09), nova linha (\x0A) e retorno de carro (\x0D).
_RE_CHARS_ILEGAIS = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")

def sanitizar(texto: str) -> str:
    return _RE_CHARS_ILEGAIS.sub("", str(texto))


# ── LEIS PERMITIDAS POR CATEGORIA (para validação) ────────────────────────────
# Extraídas automaticamente da BASE_CONHECIMENTO para evitar duplicação.

LEIS_PERMITIDAS: dict[str, set[str]] = {
    categoria: {lei["nome"] for lei in dados["leis"]}
    for categoria, dados in BASE_CONHECIMENTO.items()
}


# ── VALIDAÇÃO DE LEIS ─────────────────────────────────────────────────────────

def _tokens_da_lei(nome: str) -> list[str]:
    """
    Deriva identificadores curtos e robustos a partir do nome completo de uma lei.
    Permite reconhecer a lei mesmo que a IA use abreviações ou reformulações leves.
    Ordem de prioridade: nome completo > número da lei > número do artigo > siglas.
    """
    tokens = [nome.lower()]

    # Número de lei federal: "14.155/2021", "13.709/2018", "11.340/2006"
    for m in re.finditer(r'\d[\d.]+/\d{4}', nome):
        tokens.append(m.group(0).lower())

    # Número de artigo isolado: "Art. 171", "Art. 154-A", "Art. 218-C", "Arts. 138"
    for m in re.finditer(r'\barts?\.?\s*([\d]+-?[A-Z]?)\b', nome, re.IGNORECASE):
        numero = m.group(1)
        tokens.append(f'art. {numero.lower()}')
        tokens.append(f'art {numero.lower()}')
        tokens.append(f'artigo {numero.lower()}')

    # Siglas e termos distintos
    for kw in ['cdc', 'lgpd', 'maria da penha', 'carolina dieckmann']:
        if kw in nome.lower():
            tokens.append(kw)

    return list(dict.fromkeys(tokens))  # remove duplicatas preservando ordem


def validar_leis(base_legal_texto: str, categoria: str) -> tuple[str, bool]:
    """
    Verifica se as leis mencionadas em Base_Legal pertencem ao conjunto
    permitido para a categoria.

    Estratégia: para cada lei permitida, tenta reconhecê-la no texto usando
    múltiplos identificadores (nome completo, número da lei, número do artigo,
    siglas). Leis não reconhecidas são ignoradas; o campo fica em branco se
    nenhuma lei válida for encontrada.

    Retorna:
        (base_legal_limpa, houve_lei_invalida)
    """
    permitidas = LEIS_PERMITIDAS.get(categoria, set())

    if not permitidas:
        # categoria Seguro — não tem leis, qualquer coisa é inválida
        tem_invalida = bool(base_legal_texto.strip())
        return ("", tem_invalida)

    texto = base_legal_texto.lower()
    leis_validas_encontradas = []
    for lei in permitidas:
        tokens = _tokens_da_lei(lei)
        if any(tok in texto for tok in tokens):
            leis_validas_encontradas.append(lei)

    houve_invalida = len(leis_validas_encontradas) == 0 and bool(base_legal_texto.strip())
    base_legal_limpa = "; ".join(leis_validas_encontradas) if leis_validas_encontradas else ""

    return (base_legal_limpa, houve_invalida)


# ── CHAMADA À OPENAI ──────────────────────────────────────────────────────────

def analisar_mensagem(mensagem: str, categoria: str, score: float, api_key: str = "") -> dict:
    """
    Monta o prompt RAG e chama a OpenAI Responses API com Structured Outputs.
    Retorna o dicionário com os campos gerados, já com leis validadas.
    """
    resultado_vazio = {
        "Motivo": "",
        "Base_Legal": "",
        "Acoes_Recomendadas": "",
        "Lei_Invalida_Detectada": False,
        "Erro": "",
    }

    try:
        client = OpenAI(api_key=api_key) if api_key else _client_padrao
        messages = montar_prompt(mensagem, categoria, score)

        # Schema JSON estrito para Structured Outputs
        schema = {
            "type": "json_schema",
            "json_schema": {
                "name": "resultado_analise",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "Categoria":          {"type": "string"},
                        "Motivo":             {"type": "string"},
                        "Base_Legal":         {"type": "string"},
                        "Acoes_Recomendadas": {"type": "string"},
                    },
                    "required": ["Categoria", "Motivo", "Base_Legal", "Acoes_Recomendadas"],
                    "additionalProperties": False,
                },
            },
        }

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            response_format=schema,
        )

        content = response.choices[0].message.content
        parsed  = json.loads(content)

        # Validação de leis
        base_legal_raw   = parsed.get("Base_Legal", "")
        base_legal_limpa, houve_invalida = validar_leis(base_legal_raw, categoria)

        return {
            "Motivo":                  sanitizar(parsed.get("Motivo", "")),
            "Base_Legal":              sanitizar(base_legal_limpa),
            "Acoes_Recomendadas":      sanitizar(parsed.get("Acoes_Recomendadas", "")),
            "Lei_Invalida_Detectada":  houve_invalida,
            "Erro":                    "",
        }

    except json.JSONDecodeError as e:
        print(f"  [ERRO JSON] {e}")
        return {**resultado_vazio, "Erro": f"JSONDecodeError: {e}"}

    except Exception as e:
        print(f"  [ERRO API] {e}")
        return {**resultado_vazio, "Erro": str(e)}


# ── PIPELINE PRINCIPAL ────────────────────────────────────────────────────────

def main():
    # 1. Carrega dataset e sorteia N_POR_GRUPO exemplos por (Categoria x Dataset)
    print(f"Carregando {ARQUIVO_ENTRADA}...")
    df_full = pd.read_excel(ARQUIVO_ENTRADA)

    colunas_necessarias = {"Mensagem", "Categoria", "Dataset"}
    if not colunas_necessarias.issubset(df_full.columns):
        raise ValueError(f"O dataset precisa ter as colunas: {colunas_necessarias}")

    # Remove linhas sem mensagem, categoria ou dataset
    df_full = df_full.dropna(subset=["Mensagem", "Categoria", "Dataset"])
    df_full = df_full[df_full["Mensagem"].str.strip() != ""]

    # Amostragem: N_POR_GRUPO exemplos por combinação (Categoria x Dataset)
    amostras = []
    grupos = df_full.groupby(["Categoria", "Dataset"])
    for (cat, ds), subset in grupos:
        n = min(N_POR_GRUPO, len(subset))
        amostras.append(subset.sample(n=n, random_state=42))

    df = pd.concat(amostras).reset_index(drop=True)
    total_grupos = len(grupos)
    print(f"Grupos (Categoria x Dataset): {total_grupos}")
    print(f"Total de exemplos a processar: {len(df)}  ({N_POR_GRUPO} por grupo)\n")
    print(df.groupby(["Categoria", "Dataset"]).size().to_string())
    print()

    # 2. Prepara colunas de saída (ou retoma progresso anterior)
    for col in ["Motivo", "Base_Legal", "Acoes_Recomendadas", "Erro"]:
        df[col] = ""
    df["Lei_Invalida_Detectada"] = False
    df["Categoria_BERT"] = ""

    # Tenta carregar progresso salvo (arquivo de saída ou backup mais recente)
    import glob, os
    candidatos = sorted(
        glob.glob("backup_rag_*.xlsx") + ([ARQUIVO_SAIDA] if os.path.exists(ARQUIVO_SAIDA) else []),
        key=os.path.getmtime,
    )
    if candidatos:
        arquivo_retomada = candidatos[-1]
        try:
            df_retomada = pd.read_excel(arquivo_retomada)
            cols_retomada = ["Motivo", "Base_Legal", "Acoes_Recomendadas",
                             "Erro", "Lei_Invalida_Detectada", "Categoria_BERT"]
            if all(c in df_retomada.columns for c in cols_retomada) and len(df_retomada) == len(df):
                for col in cols_retomada:
                    df[col] = df_retomada[col].values
                # Garante dtypes corretos para evitar erro ao gravar nas colunas
                for col in ["Motivo", "Base_Legal", "Acoes_Recomendadas", "Erro", "Categoria_BERT"]:
                    df[col] = df[col].astype(object).where(df[col].notna(), "")
                df["Lei_Invalida_Detectada"] = df["Lei_Invalida_Detectada"].fillna(False).astype(bool)
                ja_feitos = (df["Motivo"].fillna("").str.strip() != "").sum()
                print(f"Retomando de '{arquivo_retomada}' — {ja_feitos} linhas já processadas.\n")
            else:
                print("Arquivo de retomada incompatível (tamanho ou colunas), começando do zero.\n")
        except Exception as e:
            print(f"Não foi possível carregar retomada ({e}), começando do zero.\n")

    # 3. Processa cada linha
    invalidas_total = int((df["Lei_Invalida_Detectada"] == True).sum())

    for i, row in df.iterrows():
        # Pula linhas já processadas (Motivo preenchido e sem erro grave)
        if str(df.at[i, "Motivo"]).strip() != "" and str(df.at[i, "Erro"]).strip() == "":
            continue
        mensagem  = str(row["Mensagem"])
        categoria = str(row["Categoria"])
        dataset   = str(row["Dataset"])

        categoria_bert, score_bert = classificar_mensagem(mensagem)

        print(f"[{i+1:02d}/{len(df)}] {categoria[:25]:<25} | BERT: {categoria_bert[:25]:<25} | {mensagem[:35]}...")

        resultado = analisar_mensagem(mensagem, categoria_bert, score_bert)

        df.at[i, "Categoria_BERT"]         = categoria_bert
        df.at[i, "Motivo"]                 = resultado["Motivo"]
        df.at[i, "Base_Legal"]             = resultado["Base_Legal"]
        df.at[i, "Acoes_Recomendadas"]     = resultado["Acoes_Recomendadas"]
        df.at[i, "Lei_Invalida_Detectada"] = resultado["Lei_Invalida_Detectada"]
        df.at[i, "Erro"]                   = resultado["Erro"]

        if resultado["Lei_Invalida_Detectada"]:
            invalidas_total += 1
            print(f"  ⚠ Lei inválida detectada — campo Base_Legal deixado em branco.")

        if resultado["Erro"]:
            print(f"  ✗ Erro: {resultado['Erro']}")

        # Backup parcial
        if (i + 1) % BACKUP_A_CADA == 0:
            backup_path = f"backup_rag_{i+1}.xlsx"
            df.to_excel(backup_path, index=False)
            print(f"  → Backup salvo: {backup_path}")

        time.sleep(1)  # respeita rate limit

    # 4. Salva resultado final
    df.to_excel(ARQUIVO_SAIDA, index=False)

    # 5. Resumo
    erros_total = (df["Erro"] != "").sum()
    print("\n" + "=" * 60)
    print(f"Concluído! {len(df)} exemplos processados.")
    print(f"  Leis inválidas detectadas : {invalidas_total}")
    print(f"  Erros de API/JSON         : {erros_total}")
    print(f"  Arquivo salvo             : {ARQUIVO_SAIDA}")
    print("=" * 60)


if __name__ == "__main__":
    main()