# VeritaPlugin — Detecção de Golpes Digitais no Facebook com BERTimbau e RAG Jurídico

**Artigo relacionado:** *VeritaPlugin: Uma Extensão de Navegador para Detecção Semântica de Fraudes no Facebook* — Universidade Federal Fluminense (UFF)

**Link Artigo SBSeg:** https://sol.sbc.org.br/index.php/sbseg/article/view/44359/44122

**Site:** https://verita-plugin-web-site.vercel.app/#hero

**Resumo do artigo.** A Engenharia Social em redes sociais explora vulnerabilidades para
iludir usuários, tornando defesas técnicas tradicionais insuficientes. Este trabalho
apresenta o VeritaPlugin, uma extensão de navegador que detecta fraudes no Facebook por
meio de um pipeline híbrido BERTimbau, RAG determinístico e GPT-4o. A arquitetura opera em
conformidade com a LGPD e o resultado apresenta ao usuário a categoria do golpe,
enquadramento legal e ações recomendadas. Para calibração, foi construído e disponibilizado
o dataset BrScamsFacebook, com 450 instâncias de golpes reais do contexto brasileiro. Na
avaliação técnica, o classificador obteve F1-macro de 0,763 ± 0,034 na validação cruzada
k=5, superando o baseline.

**Abstract.** Social engineering on social networks exploits vulnerabilities to deceive
users, rendering traditional technical defenses insufficient. This work presents
VeritaPlugin, a browser extension that detects fraud on Facebook through a hybrid pipeline
using BERTimbau, deterministic RAG, and GPT-4o. The architecture operates in compliance
with the LGPD (Brazilian General Data Protection Law), and the result presents the user
with the scam category, legal framework, and recommended actions. For calibration, the
BrScamsFacebook dataset was built and made available, containing 450 instances of real
scams from the Brazilian context. In the technical evaluation, the classifier obtained an
F1-macro of 0.763 ± 0.034 in the k=5 cross-validation, exceeding the baseline.

**Resumo do artefato.** O VeritaPlugin é uma extensão para Google Chrome que detecta
golpes digitais em publicações do Facebook em tempo real. O artefato combina dois
componentes: (i) um classificador **BERTimbau** (`bert-base-portuguese-cased`) ajustado
por *fine-tuning* sobre o dataset **BrScamsFacebook** (450 instâncias rotuladas), que
atribui a publicação a uma de 6 categorias de golpe; e (ii) um **pipeline RAG jurídico**
que recupera de uma base de conhecimento curada a legislação brasileira aplicável àquela
categoria e a injeta no contexto do GPT-4o, restringindo o espaço de resposta do modelo
para evitar a alucinação de dispositivos legais inexistentes. O resultado é entregue ao
usuário como um modal na própria página do Facebook, contendo a categoria detectada, o
motivo da suspeita, a base legal aplicável e as ações recomendadas. Este repositório
contém a API REST (FastAPI), a extensão Chrome e as instruções para execução local e
reprodução das reivindicações do artigo.

**Autora:** Bruna Norões — brunanoroes@id.uff.br

---

# Estrutura do readme.md

Este README segue os requisitos mínimos do Comitê Técnico de Artefatos do SBSeg 2026 e
está organizado nas seguintes seções:

| Seção | Conteúdo |
|---|---|
| **Título projeto** | Identificação do artefato, vínculo com o artigo e resumo |
| **Estrutura do readme.md** | Esta seção — mapa do documento e organização do repositório |
| **Selos Considerados** | Selos pleiteados na avaliação |
| **Informações básicas** | Ambiente de execução, requisitos de hardware e software, arquitetura do sistema e estrutura de arquivos |
| **Dependências** | Versões de linguagem, bibliotecas, modelos e recursos de terceiros |
| **Preocupações com segurança** | Riscos para o avaliador e medidas de mitigação |
| **Instalação** | Passo a passo para obter e instalar a API e a extensão |
| **Teste mínimo** | Execução mínima que demonstra o funcionamento do artefato |
| **Experimentos** | Reprodução das reivindicações do artigo, uma subseção por reivindicação |
| **LICENSE** | Licença do artefato |

## Organização do repositório

```
VeritaPlugin/
├── api.py                   # Servidor FastAPI — ponto de entrada da API REST
├── classificador_bert.py    # Inferência com o modelo BERTimbau (categoria + score)
├── pipeline_rag.py          # Pipeline RAG: montagem de contexto, chamada ao GPT-4o
│                            #   e validação das leis citadas
├── base_conhecimento.py     # Base de conhecimento jurídica curada, por categoria
├── download_model.py        # Baixa os pesos do modelo do HuggingFace
├── requirements.txt         # Dependências Python com versões fixadas
├── railway.toml             # Configuração do deploy (Railway)
├── nixpacks.toml            # Configuração de build do ambiente de deploy
├── modelo_bert/             # Config e tokenizer do modelo
│                            #   (model.safetensors é baixado do HuggingFace)
├── verita-plugin/           # Extensão Chrome (Manifest V3)
│   ├── manifest.json        # Permissões, content scripts e service worker
│   ├── background.js        # Service worker — intermedia as chamadas à API
│   ├── content.js           # Injeta o botão flutuante, o modo de seleção e o modal
│   ├── setup.html / setup.js# Wizard de configuração da chave da OpenAI
│   ├── bootstrap.min.css    # Estilos do modal
│   └── icon.png
├── LICENSE
└── README.md
```

## Repositórios complementares do mesmo trabalho

O artefato principal é este repositório. Os repositórios abaixo sustentam reivindicações
específicas do artigo e são referenciados na seção **Experimentos**:

| Repositório | Papel no trabalho |
|---|---|
| [treinamento-BERTimbau](https://github.com/brunanoroes/treinamento-BERTimbau) | Fine-tuning e avaliação do classificador (holdout e k-fold) |
| [Treinamento_TF-IDF-SVM](https://github.com/brunanoroes/Treinamento_TF-IDF-SVM) | Baseline TF-IDF + LinearSVC, sob o mesmo protocolo de avaliação |
| [evolucao-prompt-RAG](https://github.com/brunanoroes/evolucao-prompt-RAG) | Evolução do pipeline de *prompt engineering* e RAG (V1 → V2 → V3) |
| [ReplicaTesteFacebook](https://github.com/brunanoroes/ReplicaTesteFacebook) | Réplica local da interface do Facebook, para teste da extensão sem conta real |
| [ConteudoExtraVeritaPlugin](https://github.com/brunanoroes/ConteudoExtraVeritaPlugin) | Dataset interno de validação (capturas de tela rotuladas) |
| [scraping-scamwarners](https://github.com/brunanoroes/scraping-scamwarners), [tradutor-dataset-phishing](https://github.com/brunanoroes/tradutor-dataset-phishing), [extrator-dataset-processed_texts](https://github.com/brunanoroes/extrator-dataset-processed_texts), [tratamento-dados-golpes-lojas-falsas](https://github.com/brunanoroes/tratamento-dados-golpes-lojas-falsas) | Coleta, tradução e consolidação das fontes que compõem o BrScamsFacebook |

Recursos externos:

- **Modelo treinado:** [huggingface.co/brunanoroes/veritaplugin-bert](https://huggingface.co/brunanoroes/veritaplugin-bert)
- **Dataset BrScamsFacebook:** [kaggle.com/datasets/brunaassisgt/brscamsfacebook](https://www.kaggle.com/datasets/brunaassisgt/brscamsfacebook)

---

# Selos Considerados

Os selos considerados são: **Artefatos Disponíveis (SeloD)**, **Artefatos Funcionais
(SeloF)**, **Artefatos Sustentáveis (SeloS)** e **Experimentos Reprodutíveis (SeloR)**.

| Selo | Onde é atendido neste README |
|---|---|
| **Disponíveis (D)** | Repositório público e estável no GitHub, com este README e licença MIT |
| **Funcionais (F)** | Seções *Dependências*, *Informações básicas*, *Instalação* e *Teste mínimo* |
| **Sustentáveis (S)** | Código modularizado em quatro componentes com responsabilidade única (`api.py`, `classificador_bert.py`, `pipeline_rag.py`, `base_conhecimento.py`), documentados na seção *Informações básicas* |
| **Reprodutíveis (R)** | Seção *Experimentos*, com uma subseção por reivindicação do artigo |

---

# Informações básicas

## Ambiente de execução

O artefato foi desenvolvido e validado no seguinte ambiente:

| Item | Especificação usada no desenvolvimento |
|---|---|
| Sistema operacional | Windows 11 (também validado em Ubuntu 22.04 LTS) |
| Python | 3.10.x |
| Navegador | Google Chrome 120 ou superior (qualquer navegador Chromium com Manifest V3) |
| Deploy da API | Railway (Nixpacks), plano gratuito |
| Treinamento do modelo | Google Colaboratory, GPU NVIDIA Tesla T4 (16 GB VRAM) |

A **execução e a avaliação do artefato não exigem GPU**. A inferência do BERTimbau roda
em CPU (`torch==2.4.0+cpu`); a GPU só foi necessária na etapa de treinamento, que está
documentada no repositório `treinamento-BERTimbau`.

## Requisitos de hardware

| Recurso | Mínimo | Recomendado |
|---|---|---|
| CPU | 2 núcleos x86-64 | 4 núcleos |
| RAM | 4 GB | 8 GB |
| Disco | 3 GB livres (pesos do modelo ≈ 416 MB + dependências PyTorch ≈ 1,5 GB) | 5 GB |
| Rede | Necessária — download do modelo (HuggingFace) e chamadas à API da OpenAI | — |
| GPU | Não necessária | — |

## Requisitos de software

- Python 3.10 ou superior, com `pip`
- Google Chrome (ou Chromium) com suporte a Manifest V3
- Git
- Uma chave de API da OpenAI com acesso ao modelo `gpt-4o` e crédito disponível
  (ver *Preocupações com segurança*)

## Arquitetura do sistema

```
 Publicação do Facebook selecionada pelo usuário
             │
             ▼
 ┌───────────────────────────┐
 │  Extensão Chrome           │  content.js extrai o texto da publicação
 │  (verita-plugin/)          │  background.js envia texto + chave à API
 └───────────────────────────┘
             │  POST /VeritaPlugin/CategorizeData
             ▼
 ┌───────────────────────────┐
 │  API FastAPI (api.py)      │  valida a requisição e orquestra os componentes
 └───────────────────────────┘
             │
             ├──────────────────────────────┐
             ▼                              │
 ┌───────────────────────────┐              │
 │  classificador_bert.py    │              │
 │  BERTimbau fine-tuned     │              │
 │  → (categoria, score)     │              │
 └───────────────────────────┘              │
             │  categoria                   │
             ▼                              │
 ┌───────────────────────────┐              │
 │  base_conhecimento.py     │  recupera definição, modus operandi, leis
 │  BASE_CONHECIMENTO        │  aplicáveis e ações, para aquela categoria
 └───────────────────────────┘
             │  contexto jurídico injetado no prompt
             ▼
 ┌───────────────────────────┐
 │  pipeline_rag.py          │  monta o prompt, chama o GPT-4o com Structured
 │  → GPT-4o (JSON Schema)   │  Outputs e valida as leis citadas na resposta,
 │  → validar_leis()         │  removendo qualquer citação fora do contexto
 └───────────────────────────┘
             │
             ▼
 { categoria, risco, explicacao, baseLegal, acaoRecomendada }
             │
             ▼
 Modal exibido na própria página do Facebook
```

## Componentes e responsabilidades

| Arquivo | Responsabilidade |
|---|---|
| `api.py` | Expõe os endpoints REST, valida a entrada (mensagem não vazia, chave presente), orquestra classificador e pipeline, e converte o resultado interno no contrato de resposta da extensão |
| `classificador_bert.py` | Carrega o modelo e o tokenizer uma única vez e expõe `classificar_mensagem(texto) -> (categoria, score)` |
| `base_conhecimento.py` | Estrutura `BASE_CONHECIMENTO`, com o conhecimento jurídico curado por categoria, e `montar_prompt()`, que constrói o contexto RAG |
| `pipeline_rag.py` | `analisar_mensagem()` — chamada ao GPT-4o com saída estruturada, e `validar_leis()`, que descarta dispositivos legais não presentes na base de conhecimento |
| `download_model.py` | Baixa `model.safetensors` do HuggingFace se ainda não estiver em `modelo_bert/` |
| `verita-plugin/content.js` | Injeta o botão flutuante, controla o modo de seleção de publicação e renderiza o modal de resultado |
| `verita-plugin/background.js` | *Service worker*; lê a chave do `chrome.storage.local` e faz a requisição à API |
| `verita-plugin/setup.js` | Wizard de primeira execução, para cadastro da chave da OpenAI |

## Categorias detectadas

| Rótulo | Categoria | Descrição |
|---|---|---|
| 0 | Golpes Baseados em Relacionamento | Manipulação emocional para obtenção de vantagem |
| 1 | Golpes de Ganho Financeiro Ilusório | Promessas falsas de dinheiro fácil ou prêmios |
| 2 | Ataques de Phishing e Roubo de Dados | Coleta indevida de dados pessoais |
| 3 | Fraudes em Lojas Virtuais Falsas | Lojas online fraudulentas |
| 4 | Golpes de Desinformação Digital | Notícias falsas com fins maliciosos |
| 5 | Seguro | Conteúdo sem indícios de golpe |

## Contrato da API

**`POST /VeritaPlugin/CategorizeData`**

Requisição:
```json
{
  "message": "Parabéns! Você ganhou R$5.000. Clique aqui para resgatar.",
  "api_key": "sk-..."
}
```

Resposta (HTTP 200):
```json
{
  "categoria": "Golpes de Ganho Financeiro Ilusório",
  "risco": 91,
  "explicacao": "A mensagem promete ganho financeiro inesperado...",
  "baseLegal": "Art. 171 do Código Penal (Estelionato); Lei nº 14.155/2021",
  "acaoRecomendada": "Não clique em links suspeitos. Registre um boletim de ocorrência..."
}
```

Códigos de erro: `400` mensagem vazia · `401` chave da OpenAI ausente · `502` falha na
chamada ao GPT-4o.

**`GET /VeritaPlugin/health`** → `{ "status": "ok" }`

---

# Dependências

## Linguagem e runtime

| Dependência | Versão |
|---|---|
| Python | 3.10+ |
| pip | 22+ |
| Google Chrome / Chromium | 120+ (Manifest V3) |

## Bibliotecas Python

Declaradas em `requirements.txt` e instaladas com um único comando (ver *Instalação*):

| Biblioteca | Versão | Finalidade |
|---|---|---|
| `fastapi` | mais recente | Framework da API REST |
| `uvicorn` | mais recente | Servidor ASGI |
| `torch` | `2.4.0+cpu` | Backend de inferência do BERTimbau (build CPU, via índice extra do PyTorch) |
| `transformers` | `4.44.2` | Carregamento do modelo e do tokenizer |
| `safetensors` | mais recente | Formato dos pesos do modelo |
| `openai` | mais recente | Cliente da API do GPT-4o |
| `huggingface_hub` | mais recente | Download dos pesos do modelo |
| `pandas`, `openpyxl` | mais recente | Manipulação dos datasets |
| `python-dotenv` | mais recente | Leitura do arquivo `.env` |
| `numpy` | `<2` | Compatibilidade com `torch 2.4.0` |

> `torch==2.4.0+cpu` é resolvido através do índice extra
> `https://download.pytorch.org/whl/cpu`, já declarado no `requirements.txt`. Não é
> necessário nenhum passo manual adicional.

## Modelo

| Recurso | Origem | Tamanho |
|---|---|---|
| `veritaplugin-bert` (pesos fine-tuned) | [huggingface.co/brunanoroes/veritaplugin-bert](https://huggingface.co/brunanoroes/veritaplugin-bert) | ≈ 416 MB |
| Modelo base | [neuralmind/bert-base-portuguese-cased](https://huggingface.co/neuralmind/bert-base-portuguese-cased) | — |

O download é feito automaticamente por `download_model.py`, sem necessidade de
autenticação no HuggingFace (repositório público).

## Recursos de terceiros

| Recurso | Como obter | Custo |
|---|---|---|
| **Chave de API da OpenAI** | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) — requer conta e crédito | ≈ US$ 0,01 por análise (`gpt-4o`) |

> A chave da OpenAI é o **único recurso de terceiros com restrição de acesso** neste
> artefato. Caso o Comitê Técnico de Artefatos prefira não utilizar chave própria, uma
> chave temporária com crédito limitado pode ser fornecida através do apêndice privado
> submetido no HotCRP.

## Benchmarks e datasets

| Dataset | Instâncias | Origem |
|---|---|---|
| **BrScamsFacebook** | 450 (75 por categoria) | [Kaggle](https://www.kaggle.com/datasets/brunaassisgt/brscamsfacebook) — construído neste trabalho a partir das fontes consolidadas nos repositórios de `geracao-dataset` |

---

# Preocupações com segurança

A execução deste artefato **não oferece risco à máquina do avaliador**: não há execução
de código malicioso, não há necessidade de privilégios administrativos e nenhuma
alteração é feita fora do diretório do projeto e do perfil do navegador. Ainda assim, os
pontos abaixo devem ser observados.

## 1. Chave de API da OpenAI e custo financeiro

A extensão exige uma chave de API da OpenAI, informada pelo avaliador no wizard de
configuração. Considerações:

- A chave é armazenada **exclusivamente no navegador**, em `chrome.storage.local`. Ela
  **nunca é persistida no servidor** — a API a recebe no corpo da requisição, usa na
  chamada ao GPT-4o e a descarta.
- Cada análise consome tokens da OpenAI, com custo aproximado de **US$ 0,01 por
  publicação analisada** (`gpt-4o`). O teste mínimo descrito neste README consome menos
  de US$ 0,05.
- **Recomendação:** utilize uma chave dedicada, com limite de gasto configurado no painel
  da OpenAI, e revogue-a ao fim da avaliação.

## 2. Conteúdo do dataset

O dataset BrScamsFacebook e o dataset interno de validação contêm **textos reais de
golpes**, incluindo links maliciosos e números de telefone. **Não acesse os links nem
entre em contato com os números** presentes nos dados. Os textos são fornecidos apenas
como entrada para classificação.

## 3. Permissões da extensão

A extensão declara, em `manifest.json`, as permissões `activeTab`, `scripting`, `storage`
e `tabs`, além de `host_permissions` restritas a `*.facebook.com`, `*.railway.app` e
`localhost:8080`. Ela **não lê publicações automaticamente**: o texto só é capturado
quando o avaliador entra no modo de seleção e clica explicitamente sobre uma publicação.
Nenhum dado de navegação é coletado, armazenado ou transmitido para além da chamada à
API descrita acima.

## 4. Uso de conta real do Facebook

Não é necessário — nem recomendado — usar uma conta real do Facebook para avaliar o
artefato. O repositório [ReplicaTesteFacebook](https://github.com/brunanoroes/ReplicaTesteFacebook)
fornece uma réplica local estática da interface, suficiente para exercitar todo o fluxo
da extensão. O caminho com réplica local é o recomendado na seção *Teste mínimo*.

## 5. Escopo do resultado

O artefato é um protótipo de pesquisa acadêmica. As análises jurídicas geradas **não
substituem orientação jurídica profissional** e podem conter erros.

---

# Instalação

O tempo total de instalação é de aproximadamente **10 minutos**, dos quais a maior parte
é o download das dependências do PyTorch e dos pesos do modelo.

## Passo 1 — Obter o repositório

```bash
git clone https://github.com/brunanoroes/VeritaPlugin.git
cd VeritaPlugin
```

## Passo 2 — Criar o ambiente virtual e instalar as dependências

Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

> Tempo esperado: 3–6 minutos. Espaço em disco: ≈ 1,5 GB.

## Passo 3 — Baixar os pesos do modelo

```bash
python download_model.py
```

Saída esperada:
```
Baixando modelo de brunanoroes/veritaplugin-bert...
Modelo baixado com sucesso!
```

> Tempo esperado: 1–3 minutos, dependendo da conexão. Espaço em disco: ≈ 416 MB.
> Se o arquivo `modelo_bert/model.safetensors` já existir, o script imprime
> `Modelo já presente, pulando download.` e encerra.

## Passo 4 — Configurar a chave da OpenAI

Crie um arquivo `.env` na raiz do repositório:

```bash
echo "OPENAI_API_KEY=sk-sua-chave-aqui" > .env
```

> Este passo é opcional para a API (a extensão envia a chave em cada requisição), mas é
> **necessário** para os testes via `curl` descritos nas seções seguintes.

## Passo 5 — Subir a API localmente

```bash
python api.py
```

Saída esperada:
```
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

> A primeira requisição carrega o modelo em memória e leva ≈ 10 segundos. As seguintes
> respondem em 2–4 segundos (dominadas pela latência da OpenAI). Uso de RAM: ≈ 1,5 GB.

**Alternativa sem instalação local:** a API está publicada em
`https://veritaplugin-production.up.railway.app` e a extensão aponta para esse endereço
por padrão. Nesse caso os passos 2, 3 e 5 podem ser dispensados, sendo necessário apenas
instalar a extensão (passo 6).

## Passo 6 — Instalar a extensão no Chrome

1. Abra `chrome://extensions/`
2. Ative o **Modo do desenvolvedor** (canto superior direito)
3. Clique em **Carregar sem compactação**
4. Selecione a pasta `verita-plugin/` deste repositório
5. O wizard de configuração abre automaticamente — informe sua chave da OpenAI e salve

Ao final deste passo, o ícone do VeritaPlugin aparece na barra de extensões e a extensão
está pronta para uso.

---

# Teste mínimo

Esta seção descreve dois testes independentes. O **Teste A** valida a API isoladamente
(≈ 1 minuto) e o **Teste B** valida o fluxo completo, incluindo a extensão (≈ 5 minutos).

## Teste A — API (verificação de instalação)

Com a API rodando (Passo 5 da instalação), em outro terminal:

**A.1 — Verificar que o serviço está no ar:**
```bash
curl http://localhost:8080/VeritaPlugin/health
```
Resultado esperado:
```json
{"status":"ok"}
```

**A.2 — Analisar uma mensagem de golpe:**
```bash
curl -X POST http://localhost:8080/VeritaPlugin/CategorizeData \
  -H "Content-Type: application/json" \
  -d '{"message":"PARABÉNS! Você foi sorteado e ganhou R$ 5.000,00. Clique no link e informe seus dados bancários para resgatar o prêmio hoje!","api_key":"sk-sua-chave-aqui"}'
```

Resultado esperado — um JSON com os cinco campos do contrato, em que:

- `categoria` = `"Golpes de Ganho Financeiro Ilusório"`
- `risco` é um inteiro alto (tipicamente acima de 80)
- `baseLegal` cita o **Art. 171 do Código Penal** e/ou a **Lei nº 14.155/2021**
- `explicacao` e `acaoRecomendada` são textos em português

**A.3 — Analisar uma mensagem legítima (controle negativo):**
```bash
curl -X POST http://localhost:8080/VeritaPlugin/CategorizeData \
  -H "Content-Type: application/json" \
  -d '{"message":"Bom dia, pessoal! Amanhã tem reunião do condomínio às 19h no salão de festas. Compareçam.","api_key":"sk-sua-chave-aqui"}'
```

Resultado esperado: `categoria` = `"Seguro"` e `baseLegal` vazio ou indicando que não há
legislação aplicável. Este caso demonstra que o pipeline **não cita leis quando não há
indício de crime** — comportamento central da reivindicação #3.

> Recursos: ≈ 1,5 GB de RAM, sem uso de disco adicional. Custo: ≈ US$ 0,02 nas duas
> chamadas.

## Teste B — Fluxo completo com a extensão

**B.1 — Subir a réplica local do Facebook** (evita o uso de conta real):

```bash
git clone https://github.com/brunanoroes/ReplicaTesteFacebook.git
cd ReplicaTesteFacebook
python -m http.server 5500
```

Abra `http://localhost:5500/index.html` no Chrome.

**B.2 — Executar a análise:**

1. Clique no botão flutuante **"Analisar Post"**, no canto inferior direito
2. A página entra em modo de seleção (as publicações ficam destacadas)
3. Clique sobre uma publicação com texto suspeito
4. Aguarde 2–4 segundos

**Resultado esperado:** um modal é exibido sobre a página contendo:

- Um cabeçalho **⚠️ ATENÇÃO** (laranja) com a categoria detectada, ou **✅ SEGURO**
  (verde) para conteúdo legítimo
- O percentual de risco
- A explicação da análise
- A base legal aplicável
- As ações recomendadas

Para sair do modo de seleção, clique em **"Sair da seleção"** ou pressione **ESC**.

**B.3 — (Opcional) Teste no Facebook real:** o mesmo procedimento funciona em
`facebook.com` com uma conta qualquer. Nenhum dado da conta é coletado — apenas o texto
da publicação clicada é enviado à API.

## Solução de problemas

| Problema | Causa provável | Solução |
|---|---|---|
| Botão "Analisar Post" não aparece | Content script não injetado | Recarregue a extensão em `chrome://extensions/` e atualize a página (F5) |
| `Failed to fetch` ao analisar | API fora do ar | Verifique `GET /VeritaPlugin/health`; confirme que `python api.py` está rodando |
| HTTP 401 | Chave da OpenAI ausente | Reabra o wizard da extensão e informe a chave, ou defina `OPENAI_API_KEY` no `.env` |
| HTTP 502 | Falha na chamada ao GPT-4o | Confirme que a chave tem crédito e acesso ao modelo `gpt-4o` |
| `OSError` ao subir a API | Pesos do modelo ausentes | Execute `python download_model.py` |
| Modal sem estilo | `bootstrap.min.css` não carregado | Confirme que o arquivo está em `verita-plugin/` e recarregue a extensão |

---

# Experimentos

Esta seção descreve como reproduzir as principais reivindicações do artigo. As
reivindicações #1, #2, #5 e #6 são reproduzidas em repositórios complementares; as
reivindicações #3 e #4 são reproduzidas neste repositório.

| # | Reivindicação | Onde reproduzir | Tempo | GPU |
|---|---|---|---|---|
| 1 | BERTimbau atinge F1-macro 0,763 ± 0,034 | [treinamento-BERTimbau](https://github.com/brunanoroes/treinamento-BERTimbau) | ≈ 3 h | sim |
| 2 | BERTimbau supera o baseline TF-IDF + SVM | [Treinamento_TF-IDF-SVM](https://github.com/brunanoroes/Treinamento_TF-IDF-SVM) | ≈ 2 min | não |
| 3 | O RAG impede citação de leis fora da base curada | este repositório + [evolucao-prompt-RAG](https://github.com/brunanoroes/evolucao-prompt-RAG) | ≈ 30 min | não |
| 4 | O sistema integrado opera em tempo real | este repositório + [ReplicaTesteFacebook](https://github.com/brunanoroes/ReplicaTesteFacebook) | ≈ 5 min | não |
| 5 | Usabilidade excelente na SUS (87,0; n = 15) | [ConteudoExtraVeritaPlugin](https://github.com/brunanoroes/ConteudoExtraVeritaPlugin) | ≈ 1 min | não |
| 6 | Justificativas jurídicas validadas por avaliadores de Direito | [ConteudoExtraVeritaPlugin](https://github.com/brunanoroes/ConteudoExtraVeritaPlugin) | ≈ 1 min | não |

**Tempo total estimado para reproduzir todas as reivindicações:** ≈ 3h40, das quais ≈ 3h
correspondem ao treinamento do BERTimbau em GPU (reivindicação #1). As demais
reivindicações juntas levam menos de 45 minutos e **não exigem GPU**. As reivindicações
**#5 e #6 são verificáveis em ≈ 2 minutos, sem GPU, sem rede e sem custo**, sendo o
caminho mais rápido para o avaliador constatar resultados do artigo.

## Reivindicações #1 — O BERTimbau fine-tuned atinge F1-macro de 0,763 ± 0,034 na classificação de golpes em português

**Onde reproduzir:** [treinamento-BERTimbau](https://github.com/brunanoroes/treinamento-BERTimbau)

**Procedimento:**
```bash
git clone https://github.com/brunanoroes/treinamento-BERTimbau.git
cd treinamento-BERTimbau
pip install transformers torch scikit-learn pandas openpyxl matplotlib seaborn
python preparar_dataset.py    # gera os splits em dados_bert/  (~30 segundos)
python treinar_bert.py        # holdout + k-fold (k=5)         (~3 horas em GPU T4)
```

**Configuração:** `neuralmind/bert-base-portuguese-cased`, learning rate `2e-5`, batch
size `16`, máximo de 4 épocas com *early stopping* (paciência 2 sobre o F1-macro de
validação), weight decay `0,01`, max length `512`, seed `42`.

**Recursos esperados:** GPU com 16 GB de VRAM (Tesla T4 no Google Colaboratory),
≈ 5 GB de disco. Sem GPU, o mesmo script roda em CPU, com tempo estimado de 20 a 30 horas
— inviável para avaliação; recomenda-se, nesse caso, verificar as métricas já
versionadas em `resultados_bert/`.

**Resultado esperado** — arquivo `resultados_bert/kfold_resultado_final.json`:

| Fold | F1-macro |
|---|---|
| 1 | 0,787 |
| 2 | 0,800 |
| 3 | 0,704 |
| 4 | 0,775 |
| 5 | 0,751 |
| **Média ± DP** | **0,763 ± 0,034** |

E, no holdout 80/10/10 (`resultados_bert/holdout_metricas.json`): acurácia 82,2%,
F1-macro 0,828, F1-weighted 0,824.

> Por se tratar de fine-tuning de rede neural, pequenas variações entre execuções são
> esperadas mesmo com seed fixa (não determinismo de kernels CUDA). O valor reproduzido
> deve cair dentro da faixa de ±1 desvio padrão reportada.

## Reivindicações #2 — O BERTimbau supera o baseline TF-IDF + SVM sob protocolo idêntico de avaliação

**Onde reproduzir:** [Treinamento_TF-IDF-SVM](https://github.com/brunanoroes/Treinamento_TF-IDF-SVM)

**Procedimento:**
```bash
git clone https://github.com/brunanoroes/Treinamento_TF-IDF-SVM.git
cd Treinamento_TF-IDF-SVM
pip install scikit-learn pandas numpy openpyxl
python treinamento.py
```

**Configuração:** `TfidfVectorizer(max_features=10000, ngram_range=(1,2),
sublinear_tf=True)` + `LinearSVC(C=1.0, max_iter=2000, random_state=42)`, avaliado com
`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` — o **mesmo protocolo e a
mesma seed** usados no BERTimbau, o que torna os números diretamente comparáveis.

**Recursos esperados:** CPU apenas, < 1 GB de RAM, ≈ 2 minutos de execução, sem GPU.

**Resultado esperado** — o script imprime, ao final, o bloco `COMPARATIVO FINAL` com as
três linhas abaixo. Por usar seed fixa e algoritmos determinísticos, este experimento é
**totalmente reproduzível**, com valores idênticos a cada execução:

| Modelo | F1-macro |
|---|---|
| Classificador por maioria | 0,048 |
| TF-IDF + LinearSVC | 0,711 ± 0,027 |
| **BERTimbau fine-tuned** | **0,763 ± 0,034** |

O ganho do BERTimbau sobre o baseline é de **+0,052 de F1-macro**, concentrado nas
categorias que dependem de compreensão contextual — *Desinformação Digital* (+0,15) e
*Seguro* (+0,13). Os intervalos de ±1 desvio padrão dos dois modelos se sobrepõem
marginalmente, de modo que a evidência favorece o modelo neural sem sustentar
superioridade categórica: o TF-IDF + SVM é um baseline forte nesta tarefa.

## Reivindicações #3 — O pipeline RAG impede a citação de dispositivos legais fora da base de conhecimento curada

Esta é a reivindicação central do componente jurídico: um LLM consultado diretamente pode
gerar citações legais plausíveis e inexistentes, e a arquitetura RAG com validação
posterior elimina esse comportamento.

**Onde reproduzir:** este repositório, mais
[evolucao-prompt-RAG](https://github.com/brunanoroes/evolucao-prompt-RAG) para a evolução
das três versões do pipeline.

**Procedimento — parte A (comportamento do artefato):**

Com a API rodando, execute uma análise para cada uma das 6 categorias e confronte o campo
`baseLegal` da resposta com a base de conhecimento:

```bash
# Exemplo — phishing
curl -X POST http://localhost:8080/VeritaPlugin/CategorizeData \
  -H "Content-Type: application/json" \
  -d '{"message":"Seu CPF foi bloqueado na Receita Federal. Acesse o link e confirme seus dados bancários em até 24h para regularizar.","api_key":"sk-..."}'
```

**Resultado esperado:** para *toda* resposta, cada dispositivo citado em `baseLegal` deve
constar na lista de leis daquela categoria em `base_conhecimento.py`. A tabela abaixo é o
gabarito de verificação:

| Categoria | Leis admissíveis em `baseLegal` |
|---|---|
| Golpes de Ganho Financeiro Ilusório | Art. 171 CP, Lei 14.155/2021, Art. 307 CP, CDC |
| Golpes de Desinformação Digital | Art. 171 CP, LGPD (Lei 13.709/2018), Arts. 138–140 CP |
| Fraudes em Lojas Virtuais Falsas | Art. 171 CP, Lei 14.155/2021, CDC, LGPD |
| Ataques de Phishing e Roubo de Dados | Art. 171 CP, Lei 14.155/2021, Art. 154-A CP, LGPD |
| Golpes Baseados em Relacionamento | Art. 171 CP, Lei 14.155/2021, Art. 158 CP, Art. 218-C CP, Lei Maria da Penha |
| Seguro | Nenhuma |

Nenhum outro dispositivo deve aparecer. A função `validar_leis()`, em `pipeline_rag.py`,
remove da resposta do GPT-4o qualquer citação que não seja reconhecida como pertencente à
base de conhecimento da categoria.

**Procedimento — parte B (evolução do pipeline):**
```bash
git clone https://github.com/brunanoroes/evolucao-prompt-RAG.git
cd evolucao-prompt-RAG
pip install openai pandas openpyxl
export OPENAI_API_KEY="sk-..."     # PowerShell: $env:OPENAI_API_KEY="sk-..."
cd analisando-resultados-v3 && python pipeline_rag.py
```

**Resultado esperado:** o arquivo `dataset_teste_rag.xlsx` é regenerado com as colunas
`Categoria`, `Motivo`, `Base_Legal` e `Acoes_Recomendadas`. Comparando-o com o
`dataset_teste_rag.xlsx` de `analisando-resultados-v2/` observa-se o efeito das duas
melhorias descritas no artigo: o reconhecimento de leis por tokenização (V3) deixa de
descartar citações válidas que o GPT-4o abreviou, e os limiares de evidência no system
prompt reduzem a citação de dispositivos sem respaldo no texto.

**Recursos esperados:** CPU apenas, < 500 MB de RAM. Tempo: ≈ 15 minutos para 30
mensagens (5 por categoria, controlado pela constante `N_POR_GRUPO`). Custo: ≈ US$ 0,30.

> Por se tratar de geração por LLM, a redação de `Motivo` e `Acoes_Recomendadas` varia
> entre execuções. O que é reprodutível — e é o objeto da reivindicação — é a
> **restrição do conjunto de leis citáveis**, verificável pelo gabarito acima.

## Reivindicações #4 — O sistema integrado opera em tempo real sobre publicações do Facebook

**Onde reproduzir:** este repositório.

**Procedimento:** execute o **Teste B** da seção *Teste mínimo*, usando a réplica local do
Facebook.

**Resultado esperado:** para cada publicação selecionada, o modal é exibido em **2 a 4
segundos**, contendo categoria, percentual de risco, explicação, base legal e ações
recomendadas. A latência é dominada pela chamada ao GPT-4o; a inferência do BERTimbau em
CPU leva menos de 200 ms.

Para validação em escala, o repositório
[ConteudoExtraVeritaPlugin](https://github.com/brunanoroes/ConteudoExtraVeritaPlugin)
contém o dataset interno de validação, com capturas de tela de publicações reais
organizadas por categoria de golpe, acompanhadas da planilha de rotulação.

**Recursos esperados:** ≈ 1,5 GB de RAM (API) + navegador. Tempo: ≈ 5 minutos. Custo:
≈ US$ 0,01 por publicação analisada.

## Reivindicações #5 — O VeritaPlugin alcança usabilidade excelente segundo a System Usability Scale

**Onde reproduzir:** [ConteudoExtraVeritaPlugin](https://github.com/brunanoroes/ConteudoExtraVeritaPlugin),
seção *Experimentos*, Reivindicação #5.

**Estudo.** Questionário **System Usability Scale (SUS)** aplicado a **15 participantes**
em experimento controlado sobre a *Facebook Replica v1.0*
([ReplicaTesteFacebook](https://github.com/brunanoroes/ReplicaTesteFacebook)), ambiente que
expôs todos os participantes aos mesmos cenários. O protocolo foi não diretivo, em duas
etapas comparativas — exploração **sem** auxílio tecnológico, para estabelecer a percepção
de risco de base, seguida de navegação **assistida** pelo VeritaPlugin —, tendo o método
*Think Aloud* como principal instrumento de observação.

**Procedimento:**
```bash
git clone https://github.com/brunanoroes/ConteudoExtraVeritaPlugin.git
cd ConteudoExtraVeritaPlugin
pip install pandas openpyxl
# execute o Teste B daquele README, que recalcula o escore a partir dos dados brutos
```

**Recursos esperados:** CPU apenas, < 512 MB de RAM, ≈ 1 minuto. Sem GPU, sem rede, sem
custo.

**Resultado esperado:**

| Métrica | Valor |
|---|---|
| Participantes | 15 |
| **Escore SUS médio** | **87,0** |
| Desvio padrão | 11,2 |
| Mediana | 87,5 |
| Mínimo / Máximo | 70,0 / 100,0 |
| Participantes acima de 68 (média da indústria) | **15 de 15** |

Na escala de referência da SUS, 68 é a média da indústria e valores acima de 80,3
correspondem à faixa "excelente" (grau A). O escore de 87,0 situa-se nessa faixa, e nenhum
participante atribuiu escore abaixo da média da indústria. O item menos favorável foi
*"Considerei o VeritaPlugin mais complexo do que o necessário"* (média 2,53 numa escala de
5, com polaridade invertida), indicando que parte dos participantes percebeu complexidade
acima do ideal — o principal ponto de melhoria identificado.

**Determinismo:** total. O cálculo é aritmética simples sobre um arquivo de dados fixo.

## Reivindicações #6 — As justificativas jurídicas geradas pelo pipeline RAG são consideradas adequadas por avaliadores com formação em Direito

**Onde reproduzir:** [ConteudoExtraVeritaPlugin](https://github.com/brunanoroes/ConteudoExtraVeritaPlugin),
seção *Experimentos*, Reivindicação #6.

**Estudo.** **4 avaliadores** com formação (concluída ou em curso) em Direito avaliaram as
saídas do **pipeline RAG v3** sobre **18 casos**, totalizando 72 avaliações por critério.
Cada justificativa foi julgada quanto a pertinência legal, correção jurídica e
proporcionalidade, além de uma questão de síntese sobre sua adequação a um usuário leigo.

**Procedimento:** execute o **Teste C** do README daquele repositório, que recalcula as
distribuições a partir dos dados brutos.

**Recursos esperados:** CPU apenas, < 512 MB de RAM, ≈ 1 minuto. Sem GPU, sem rede, sem
custo.

**Resultado esperado:**

| Critério | Resultado favorável | % |
|---|---|---|
| Proporcionalidade | Proporcional à gravidade do caso | **81,9%** |
| Correção jurídica | Descrição precisa da lei | **76,4%** |
| Pertinência legal | Dispositivo diretamente aplicável | **68,1%** |
| Síntese — apresentaria a um leigo | "Sim" | **56,9%** |
| Síntese — aproveitável ("Sim" + "Com ajustes") | — | **90,3%** |
| Síntese — rejeitada ("Não") | — | 9,7% |

**Interpretação.** A proporcionalidade é o critério mais bem avaliado, e **nenhuma
avaliação apontou subestimação da gravidade** — quando o sistema erra a dosagem, erra para
mais (18,1%), comportamento consistente com o objetivo de alertar o usuário. **90,3% das
justificativas são aproveitáveis** e apenas 9,7% foram rejeitadas para apresentação a um
leigo.

Ao mesmo tempo, o resultado delimita o alcance da contribuição: que um terço das
justificativas requeira ajustes e que 13,9% dos dispositivos sejam considerados não
pertinentes confirma a ressalva mantida em todo o trabalho — as análises **não substituem
orientação jurídica profissional**.

**Determinismo:** total. São contagens sobre um arquivo de dados fixo.

**Limitação a considerar:** com 4 avaliadores, os percentuais têm intervalo de confiança
largo e não permitem calcular concordância entre avaliadores com estabilidade estatística.
Os resultados são indicativos e qualitativos.

---

# LICENSE

Este artefato é distribuído sob a **Licença MIT**. O texto completo está no arquivo
[LICENSE](LICENSE) deste repositório.

```
MIT License

Copyright (c) 2026 Bruna Norões

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions: [...]
```

O modelo base **BERTimbau** (`neuralmind/bert-base-portuguese-cased`) é distribuído por
seus autores sob licença MIT. O dataset **BrScamsFacebook** é disponibilizado no Kaggle
para fins de pesquisa acadêmica.

> Este software é um protótipo de pesquisa acadêmica. Os resultados podem conter erros e
> **não substituem orientação jurídica profissional**.
