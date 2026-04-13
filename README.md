# VeritaPlugin

Extensão do Chrome para detecção de golpes digitais no Facebook, desenvolvida como Trabalho de Conclusão de Curso (TCC).

O sistema combina um modelo **BERTimbau** treinado para classificação de golpes com um **pipeline RAG jurídico** (OpenAI GPT-4o), expondo os resultados via API REST hospedada no Railway para uma extensão do Chrome.

---

## Como funciona

```
Usuário clica em "Analisar Post" no Facebook
        ↓
Extensão entra em modo de seleção
        ↓
Usuário clica em uma publicação
        ↓
Extensão envia o texto + chave OpenAI para a API no Railway
        ↓
BERTimbau classifica → (categoria, confiança)
        ↓
Pipeline RAG monta contexto jurídico + chama OpenAI GPT-4o
        ↓
API retorna { categoria, risco, explicacao, baseLegal, acaoRecomendada }
        ↓
Extensão exibe resultado em modal na página
```

> A chave da OpenAI é inserida pelo usuário na tela de configuração da extensão e fica salva apenas no navegador (`chrome.storage.local`). Ela nunca é armazenada no servidor.

---

## Categorias detectadas

| Categoria | Descrição |
|---|---|
| Golpes de Ganho Financeiro Ilusório | Promessas falsas de dinheiro fácil ou prêmios |
| Golpes de Desinformação Digital | Notícias falsas com fins maliciosos |
| Fraudes em Lojas Virtuais Falsas | Lojas online fraudulentas |
| Ataques de Phishing e Roubo de Dados | Coleta indevida de dados pessoais |
| Golpes Baseados Em Relacionamento | Manipulação emocional para obter vantagens |
| Seguro | Conteúdo sem indícios de golpe |

---

## Estrutura do projeto

```
VeritaPlugin/
├── api.py                  # Servidor FastAPI — ponto de entrada
├── classificador_bert.py   # Inferência com o modelo BERTimbau
├── pipeline_rag.py         # Pipeline RAG + validação de leis + chamada à OpenAI
├── base_conhecimento.py    # Base de conhecimento jurídica por categoria
├── download_model.py       # Baixa o modelo do HuggingFace no deploy
├── requirements.txt        # Dependências Python
├── railway.toml            # Configuração do deploy no Railway
├── modelo_bert/            # Arquivos do modelo (model.safetensors no HuggingFace)
└── verita-plugin/          # Extensão Chrome
    ├── manifest.json
    ├── background.js
    ├── content.js
    ├── setup.html / setup.js   # Wizard de configuração
    ├── bootstrap.min.css
    └── icon.png
```

---

## Modelo BERTimbau

O modelo treinado está hospedado no HuggingFace e é baixado automaticamente no deploy:

🤗 [brunanoroes/veritaplugin-bert](https://huggingface.co/brunanoroes/veritaplugin-bert)

---

## API

A API está hospedada no Railway:

🌐 `https://veritaplugin-production.up.railway.app`

### `POST /VeritaPlugin/CategorizeData`

**Request:**
```json
{
  "message": "Parabéns! Você ganhou R$5.000. Clique aqui para resgatar.",
  "api_key": "sk-..."
}
```

**Response:**
```json
{
  "categoria": "Golpes de Ganho Financeiro Ilusório",
  "risco": 91,
  "explicacao": "A mensagem promete ganho financeiro inesperado...",
  "baseLegal": "Art. 171 do Código Penal (Estelionato); Lei nº 14.155/2021",
  "acaoRecomendada": "Não clique em links suspeitos. Registre um boletim de ocorrência..."
}
```

### `GET /VeritaPlugin/health`

```json
{ "status": "ok" }
```

---

## Instalação da extensão

### Pré-requisitos

- Google Chrome
- Chave de API da OpenAI → [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### Passos

1. Baixe ou clone este repositório
2. Abra o Chrome e acesse `chrome://extensions/`
3. Ative o **Modo do desenvolvedor** (canto superior direito)
4. Clique em **Carregar sem compactação**
5. Selecione a pasta `verita-plugin/`

Ao instalar pela primeira vez, o **wizard de configuração** abrirá automaticamente com instruções para inserir sua chave da OpenAI.

---

## Usando a extensão

1. Abra o **Facebook**
2. Clique no botão flutuante **"Analisar Post"** no canto inferior direito
3. Clique em qualquer publicação com texto suspeito
4. O resultado aparece em um modal com:
   - ✅ **SEGURO** (verde) ou ⚠️ **ATENÇÃO** (laranja) com a categoria detectada
   - Explicação da análise
   - Base legal aplicável
   - Ações recomendadas

> Para cancelar o modo de seleção, clique em **"Sair da seleção"** ou pressione **ESC**.

---

## Deploy (Railway)

O deploy é feito automaticamente via GitHub. A cada push na branch `main`, o Railway rebuilda e sobe a API.

O modelo é baixado do HuggingFace automaticamente na inicialização via `download_model.py`.

### Variáveis de ambiente no Railway

| Variável | Descrição |
|---|---|
| `OPENAI_API_KEY` | Opcional — fallback caso a chave não venha na requisição |

---

## Solução de problemas

| Problema | Solução |
|---|---|
| Botão não aparece no Facebook | Recarregue a extensão em `chrome://extensions/` |
| "Failed to fetch" ao analisar | Verifique se a API está online em `/VeritaPlugin/health` |
| Erro ao analisar | Confirme que sua chave OpenAI tem crédito disponível |
| Modal sem estilo | Verifique se `bootstrap.min.css` está na pasta `verita-plugin/` |
