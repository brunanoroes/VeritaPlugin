# VeritaPlugin

Extensão do Chrome para detecção de golpes digitais no Facebook, desenvolvida como Trabalho de Conclusão de Curso (TCC).

O sistema combina um modelo **BERTimbau** treinado para classificação de golpes com um **pipeline RAG jurídico** (OpenAI GPT-4o), expondo os resultados via API REST para a extensão.

---

## Como funciona

```
Usuário clica em "Analisar Post" no Facebook
        ↓
Extensão entra em modo de seleção
        ↓
Usuário clica em uma publicação
        ↓
Extensão envia o texto + chave OpenAI para o servidor local
        ↓
BERTimbau classifica → (categoria, confiança)
        ↓
Pipeline RAG monta contexto jurídico + chama OpenAI GPT-4o
        ↓
API retorna { categoria, risco, explicacao, baseLegal, acaoRecomendada }
        ↓
Extensão exibe resultado em modal na página
```

> A chave da OpenAI é inserida pelo usuário na tela de configuração da extensão e fica salva apenas no navegador (`chrome.storage.local`). Ela nunca é enviada a terceiros além da própria OpenAI.

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
├── requirements.txt        # Dependências Python
├── iniciar.bat             # Inicia o servidor (instala dependências na 1ª vez)
├── .env.example            # Modelo do arquivo de configuração (opcional)
├── modelo_bert/            # Modelo BERTimbau treinado (baixar separadamente)
└── verita-plugin/          # Extensão Chrome
    ├── manifest.json
    ├── background.js
    ├── content.js
    ├── popup.html / popup.js / popup.css
    ├── setup.html / setup.js   # Wizard de configuração (abre na 1ª instalação)
    ├── bootstrap.min.css
    └── icon.png
```

---

## Instalação

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

### 2. Baixar o modelo BERTimbau

O arquivo `model.safetensors` (~416 MB) não está no repositório por ser muito grande para o GitHub.

**Baixe pelo link abaixo e coloque dentro da pasta `modelo_bert/`:**

> 🔗 [Link para download do modelo](#) ← substituir pelo link real

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

### 3. Iniciar o servidor

Dê dois cliques em **`iniciar.bat`**.

Na primeira execução ele irá:
- Verificar se o Python está instalado
- Instalar todas as dependências automaticamente
- Subir o servidor em `http://localhost:8080`

> Mantenha a janela aberta enquanto usa o plugin.

---

### 4. Instalar a extensão no Chrome

1. Abra o Chrome e acesse `chrome://extensions/`
2. Ative o **Modo do desenvolvedor** (canto superior direito)
3. Clique em **Carregar sem compactação**
4. Selecione a pasta `verita-plugin/`

Ao instalar pela primeira vez, o **wizard de configuração** abrirá automaticamente guiando o usuário por todas as etapas, incluindo a inserção da chave da OpenAI.

---

## Usando a extensão

1. Com o servidor rodando (`iniciar.bat`), abra o **Facebook**
2. Clique no botão flutuante **"Analisar Post"** no canto inferior direito
3. Clique em qualquer publicação com texto suspeito
4. O resultado aparece em um modal com:
   - ✅ **SEGURO** (verde) ou ⚠️ **ATENÇÃO** (laranja) com a categoria detectada
   - Explicação da análise
   - Base legal aplicável
   - Ações recomendadas

> Para cancelar o modo de seleção, clique em **"Sair da seleção"** ou pressione **ESC**.

---

## API

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

## Solução de problemas

| Problema | Solução |
|---|---|
| Botão não aparece no Facebook | Recarregue a extensão em `chrome://extensions/` |
| "Failed to fetch" ao analisar | Verifique se o `iniciar.bat` está aberto e rodando |
| Erro ao analisar | Confirme que sua chave OpenAI tem crédito disponível |
| Servidor não inicia | Confirme que o Python está instalado e no PATH |
| Modelo não encontrado | Coloque o `model.safetensors` dentro da pasta `modelo_bert/` |
