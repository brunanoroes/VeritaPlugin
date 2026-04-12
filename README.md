# VeritaPlugin

Ferramenta de detecção de golpes digitais em redes sociais, desenvolvida como Trabalho de Conclusão de Curso (TCC).

O sistema combina um modelo **BERTimbau** treinado para classificação de golpes com um **pipeline RAG jurídico** (OpenAI GPT-4o), expondo os resultados via API REST para uma extensão do Chrome.

---

## Como funciona

```
Usuário clica em "Analisar Post" no navegador
        ↓
Extensão Chrome captura o texto selecionado
        ↓
POST /VeritaPlugin/CategorizeData { message }
        ↓
BERTimbau classifica → (categoria, confiança)
        ↓
Pipeline RAG monta contexto jurídico + chama OpenAI GPT-4o
        ↓
API retorna { categoria, risco, explicacao, baseLegal, acaoRecomendada }
        ↓
Extensão exibe resultado em modal na página
```

> A chave da OpenAI **nunca vai para a extensão**. Ela fica exclusivamente no servidor Python, no arquivo `.env` de cada pessoa.

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
ProjetoFinal/
├── api.py                  # Servidor FastAPI — ponto de entrada
├── classificador_bert.py   # Inferência com o modelo BERTimbau
├── pipeline_rag.py         # Pipeline RAG + validação de leis + chamada à OpenAI
├── base_conhecimento.py    # Base de conhecimento jurídica por categoria
├── requirements.txt        # Dependências Python
├── .env.example            # Modelo do arquivo de configuração (copiar para .env)
├── modelo_bert/            # Modelo BERTimbau treinado (baixar separadamente — ver abaixo)
└── verita-plugin/          # Extensão Chrome
    ├── manifest.json
    ├── background.js
    ├── content.js
    ├── selector.js
    ├── popup.html / popup.js / popup.css
    ├── bootstrap.min.css   # Bootstrap 5 embutido localmente
    └── icon.png
```

---

## Instalação e execução

### Pré-requisitos

- Python 3.10+
- Google Chrome
- Chave de API da OpenAI → [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

---

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/veritaplugin.git
cd veritaplugin
```

---

### 2. Instalar dependências Python

```bash
pip install -r requirements.txt
```

---

### 3. Baixar o modelo BERTimbau

O arquivo `model.safetensors` (~416 MB) não está no repositório por ser muito grande para o GitHub.

**Baixe pelo link abaixo e coloque dentro da pasta `modelo_bert/`:**

> 🔗 [Link para download do modelo](#) ← substituir pelo link real (Google Drive, HuggingFace, etc.)

A pasta deve ficar assim:

```
modelo_bert/
├── config.json
├── model.safetensors   ← baixar e colocar aqui
├── tokenizer.json
├── tokenizer_config.json
└── training_args.bin
```

---

### 4. Configurar a chave OpenAI

Copie o arquivo `.env.example` e renomeie para `.env`:

```bash
# Linux / Mac
cp .env.example .env

# Windows CMD
copy .env.example .env
```

Abra o `.env` e cole sua chave:

```
OPENAI_API_KEY=cole_sua_chave_aqui
```

> O arquivo `.env` **não é enviado ao GitHub** (está no `.gitignore`). Cada pessoa usa a própria chave.

---

### 5. Iniciar o servidor

```bash
python api.py
```

O servidor sobe em `http://localhost:8080`.
Documentação interativa disponível em `http://localhost:8080/docs`.

---

### 6. Instalar a extensão no Chrome

1. Abra o Chrome e acesse `chrome://extensions/`
2. Ative o **Modo do desenvolvedor** (canto superior direito)
3. Clique em **Carregar sem compactação**
4. Selecione a pasta `verita-plugin/`

O botão **"Analisar Post"** aparecerá em qualquer página do navegador.

---

## Usando a extensão

1. Com o servidor rodando (`python api.py`), abra qualquer página
2. Clique no botão flutuante **"Analisar Post"**
3. Clique em qualquer elemento da página com texto suspeito
4. O resultado aparece em um modal com:
   - **SEGURO** (verde) ou **ATENÇÃO** (laranja) com a categoria detectada
   - Explicação do modelo
   - Base legal aplicável
   - Ações recomendadas

---

## API

### `POST /VeritaPlugin/CategorizeData`

**Request:**
```json
{ "message": "Parabéns! Você ganhou R$5.000. Clique aqui para resgatar." }
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

## Solução de problemas

| Problema | Solução |
|---|---|
| Botão não aparece na página | Recarregue a extensão em `chrome://extensions/` |
| Modal sem estilo (sem CSS) | Verifique se `bootstrap.min.css` está na pasta `verita-plugin/` |
| Erro 502 na análise | Verifique se a chave no `.env` está correta e tem crédito na OpenAI |
| Servidor não inicia | Confirme que o modelo está em `modelo_bert/model.safetensors` |
| Plugin não conecta ao servidor | Confirme que `python api.py` está rodando e use `http://localhost:8080/docs` para testar |
