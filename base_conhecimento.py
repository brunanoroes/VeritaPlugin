"""
base_conhecimento.py
====================
Base de conhecimento legal estruturada para RAG
Sistema de Detecção de Golpes — BrScamsFacebook

Uso:
    from base_conhecimento import BASE_CONHECIMENTO, montar_contexto, montar_prompt

    contexto = montar_contexto("Fraudes em Lojas Virtuais Falsas")
    prompt   = montar_prompt(mensagem, "Fraudes em Lojas Virtuais Falsas", contexto)
"""

# ── BASE DE CONHECIMENTO ──────────────────────────────────────────────────────
# Cada categoria tem:
#   - definicao    : o que caracteriza o golpe
#   - modus_operandi: como funciona na prática
#   - leis         : lista de leis aplicáveis com descrição e pena
#   - analise      : raciocínio jurídico consolidado (síntese)
#   - acoes        : o que a vítima deve fazer

BASE_CONHECIMENTO = {

    # ── 1. GOLPES FINANCEIROS ─────────────────────────────────────────────────
    "Golpes de Ganho Financeiro Ilusório": {
        "definicao": (
            "Esquemas fraudulentos que induzem a vítima a realizar pagamentos antecipados "
            "ou ceder informações sensíveis sob falsa promessa de grande recompensa futura "
            "(prêmios, heranças, retornos de investimento). Empregam Engenharia Social "
            "explorando ingenuidade, necessidade econômica ou ganância."
        ),
        "modus_operandi": (
            "Criação de fachada de legitimidade (perfis falsos, sorteios falsos, "
            "plataformas de investimento falsas) → promessa de recompensa futura → "
            "solicitação de pagamento antecipado ou dado sensível → desaparecimento."
        ),
        "leis": [
            {
                "nome": "Art. 171 do Código Penal (Estelionato)",
                "tipo": "crime patrimonial",
                "descricao": "Obtenção de vantagem ilícita por meio de fraude, enganando a vítima.",
                "aplicacao": "Golpe do PIX, falso investimento, falsa herança, falso prêmio.",
            },
            {
                "nome": "Lei nº 14.155/2021 (Fraude Eletrônica)",
                "tipo": "crime digital",
                "descricao": "Atualiza o Código Penal para fraudes realizadas por meios digitais.",
                "aplicacao": "Golpes via redes sociais, WhatsApp, aplicativos de investimento falsos.",
            },
            {
                "nome": "Art. 307 do Código Penal (Falsa Identidade)",
                "tipo": "crime contra a fé pública",
                "descricao": "Alguém se passa por outra pessoa para obter vantagem ou causar dano.",
                "aplicacao": "Criação de perfis falsos, golpista fingindo ser banco ou empresa.",
            },
            {
                "nome": "Código de Defesa do Consumidor (CDC)",
                "tipo": "proteção ao consumidor",
                "descricao": "Protege contra propaganda enganosa e práticas abusivas comerciais.",
                "aplicacao": "Sorteios falsos, promoções inexistentes, publicidade enganosa.",
            },
        ],
        "analise": (
            "A responsabilização concentra-se no Estelionato (Art. 171) e na Fraude Eletrônica "
            "(Lei 14.155/2021), pois o objetivo é induzir ao erro para obter pagamentos antecipados. "
            "A Falsa Identidade (Art. 307) é aplicada quando criminosos clonam perfis ou usam nomes "
            "de terceiros para endossar a fraude. O CDC incide quando a conduta mimetiza sorteios "
            "ou serviços comerciais legítimos."
        ),
        "acoes": [
            "Bloquear e denunciar imediatamente o perfil ou página golpista no Facebook/Messenger/Marketplace.",
            "Se realizou transferências (Pix) ou forneceu dados de cartão, contatar a instituição financeira imediatamente para contestação e congelamento cautelar.",
            "Preservar evidências: capturas de tela de todas as conversas, anúncios e comprovantes.",
            "Registrar Boletim de Ocorrência (B.O.) em delegacia especializada em crimes cibernéticos.",
        ],
    },

    # ── 2. DESINFORMAÇÃO ──────────────────────────────────────────────────────
    "Golpes de Desinformação Digital": {
        "definicao": (
            "Criação e disseminação massiva e deliberada de informações falsas ou manipuladas, "
            "frequentemente impulsionadas por bots e contas falsas. O objetivo é obter vantagens "
            "financeiras ou influenciar a opinião pública, explorando gatilhos emocionais "
            "(medo, raiva, senso de urgência)."
        ),
        "modus_operandi": (
            "Fabricação de notícia falsa com aparência legítima → disparo massivo via bots → "
            "exploração emocional da audiência → monetização (cliques, doações, produtos falsos) "
            "ou manipulação de mercado/eleições."
        ),
        "leis": [
            {
                "nome": "Art. 171 do Código Penal (Estelionato)",
                "tipo": "crime patrimonial",
                "descricao": "Obtenção de vantagem ilícita por meio de fraude ou engano.",
                "aplicacao": (
                    "Fake news para vender curas milagrosas, manipular mercado financeiro, "
                    "ou induzir a vítima a pagar por serviços governamentais inexistentes."
                ),
            },
            {
                "nome": "LGPD (Lei nº 13.709/2018)",
                "tipo": "proteção de dados",
                "descricao": "Regula o tratamento de dados pessoais; proíbe uso de dados para manipulação política ou comercial sem consentimento.",
                "aplicacao": (
                    "Quando bots e perfis falsos coletam e utilizam dados pessoais de usuários "
                    "para segmentar e amplificar campanhas de desinformação."
                ),
            },
            {
                "nome": "Código Penal – Arts. 138 a 140",
                "tipo": "crime contra a honra",
                "descricao": (
                    "Art. 138 (Calúnia): imputar falsamente fato criminoso a alguém. "
                    "Art. 139 (Difamação): imputar fato ofensivo à reputação. "
                    "Art. 140 (Injúria): ofender a dignidade ou o decoro de alguém."
                ),
                "aplicacao": (
                    "Fake news que atribuem falsamente crimes a pessoas, mancham reputações "
                    "ou ofendem a dignidade de indivíduos identificáveis."
                ),
            },
        ],
        "analise": (
            "Quando a desinformação é usada deliberadamente como ardil para manipular o mercado "
            "financeiro, promover curas milagrosas ou induzir pagamentos por serviços inexistentes, "
            "tipifica-se como Estelionato (Art. 171 do Código Penal). A lei foca na vantagem ilícita "
            "obtida por meio da distorção deliberada da verdade para enganar o público-alvo."
        ),
        "acoes": [
            "Não clicar em links suspeitos nem compartilhar a postagem — compartilhar alimenta o algoritmo do golpista.",
            "Bloquear e denunciar o perfil ou página imediatamente pelas ferramentas da rede social.",
            "Verificar a procedência da notícia em canais oficiais ou agências de fact-checking antes de qualquer ação.",
            "Se a desinformação levou a transferências financeiras, contatar o banco imediatamente.",
            "Em caso de perda financeira ou dano à honra, reunir capturas de tela e registrar B.O. em delegacia especializada.",
        ],
    },

    # ── 3. LOJAS VIRTUAIS FALSAS ──────────────────────────────────────────────
    "Fraudes em Lojas Virtuais Falsas": {
        "definicao": (
            "Uso malicioso da infraestrutura de vendas das redes sociais (como o Marketplace) "
            "para atrair consumidores com ofertas irreais, clonando muitas vezes a identidade "
            "visual de marcas legítimas. A finalidade é receber o pagamento sem entrega do produto "
            "ou capturar dados bancários durante o falso processo de compra."
        ),
        "modus_operandi": (
            "Criação de loja ou perfil falso com fotos roubadas de produtos → preço abaixo do mercado "
            "→ pressão para pagamento via Pix ou boleto → desaparecimento após receber o pagamento, "
            "ou coleta de dados de cartão em checkout falso."
        ),
        "leis": [
            {
                "nome": "Art. 171 do Código Penal (Estelionato)",
                "tipo": "crime patrimonial",
                "descricao": "Obtenção de vantagem ilícita ao enganar outra pessoa.",
                "aplicacao": "Venda de produto que não será entregue, falso boleto, e-commerce fantasma.",
            },
            {
                "nome": "Lei nº 14.155/2021 (Fraude Eletrônica)",
                "tipo": "crime digital",
                "descricao": "Trata fraudes cometidas em ambiente digital, aumentando penas.",
                "aplicacao": "Lojas falsas no Marketplace, phishing em checkout, clonagem de sites.",
            },
            {
                "nome": "Código de Defesa do Consumidor (CDC)",
                "tipo": "proteção ao consumidor",
                "descricao": "Protege contra propaganda enganosa e garante direito de arrependimento em compras online.",
                "aplicacao": "Anúncios com informações falsas, produto inexistente, oferta enganosa.",
            },
            {
                "nome": "LGPD — Lei Geral de Proteção de Dados (Lei nº 13.709/2018)",
                "tipo": "proteção de dados",
                "descricao": "Regula coleta e uso de dados pessoais; exige consentimento e transparência.",
                "aplicacao": "Coleta abusiva de dados de cartão em checkout falso, vazamento de CPF/e-mail.",
            },
        ],
        "analise": (
            "A responsabilização penal apoia-se no Estelionato (Art. 171) e na Fraude Eletrônica "
            "(Lei 14.155/2021), punindo e-commerces fantasmas que capturam pagamentos sem intenção "
            "de entregar a mercadoria. O CDC é o pilar de defesa contra publicidade enganosa e oferta "
            "fraudulenta em redes sociais. A LGPD resguarda consumidores contra coleta abusiva de "
            "dados cadastrais e de cartão inseridos em formulários de checkout fraudulentos."
        ),
        "acoes": [
            "Interromper a negociação, bloquear e denunciar o vendedor/página no Facebook.",
            "Acionar a instituição financeira e administradora do cartão imediatamente para estorno e bloqueio do cartão.",
            "Reunir provas: capturas de tela do anúncio falso, link da loja, conversas e comprovantes de pagamento.",
            "Registrar B.O. formalizando o crime de estelionato digital.",
        ],
    },

    # ── 4. PHISHING ───────────────────────────────────────────────────────────
    "Ataques de Phishing e Roubo de Dados": {
        "definicao": (
            "Campanhas focadas na extração sistemática de dados sensíveis, credenciais de acesso "
            "e informações financeiras para fins ilícitos. Os estelionatários mimetizam instituições "
            "legítimas (bancos, redes sociais) ou usam perfis falsos para disparar links maliciosos, "
            "comprometer dispositivos ou manipular a vítima a entregar credenciais voluntariamente."
        ),
        "modus_operandi": (
            "Mensagem urgente imitando banco/rede social → link malicioso para página falsa "
            "→ vítima insere credenciais → dados capturados e usados para esvaziamento de conta "
            "ou fraudes em nome da vítima. Variante: instalação de malware por clique no link."
        ),
        "leis": [
            {
                "nome": "Art. 171 do Código Penal (Estelionato)",
                "tipo": "crime patrimonial",
                "descricao": "Obtenção de vantagem ilícita por fraude, causando prejuízo à vítima.",
                "aplicacao": "Uso das credenciais roubadas para esvaziamento de conta, compras fraudulentas.",
            },
            {
                "nome": "Lei nº 14.155/2021 (Fraude Eletrônica)",
                "tipo": "crime digital",
                "descricao": "Moderniza o Código Penal para fraudes via internet, com penas agravadas.",
                "aplicacao": "Phishing por e-mail ou redes sociais, clonagem de WhatsApp, fraudes bancárias online.",
            },
            {
                "nome": "Art. 154-A do Código Penal (Lei Carolina Dieckmann — Invasão de Dispositivo)",
                "tipo": "crime cibernético",
                "descricao": "Tipifica a invasão de dispositivos eletrônicos para obter, adulterar ou destruir dados.",
                "aplicacao": "Instalação de malware via link malicioso, hack de e-mail ou redes sociais, spyware.",
            },
            {
                "nome": "LGPD — Lei Geral de Proteção de Dados (Lei nº 13.709/2018)",
                "tipo": "proteção de dados",
                "descricao": "Regula o tratamento de dados pessoais; vazamentos facilitam golpes.",
                "aplicacao": "Uso indevido de CPF, e-mail ou dados financeiros roubados em ataques de phishing.",
            },
        ],
        "analise": (
            "O foco é a quebra da segurança da informação e violação da privacidade. A extração "
            "fraudulenta de credenciais é punida pelo Estelionato (Art. 171) e pela Fraude Eletrônica "
            "(Lei 14.155/2021). A Lei Carolina Dieckmann (Art. 154-A) criminaliza a invasão direta "
            "de dispositivos e instalação de malwares. A LGPD penaliza o tratamento ilícito e a "
            "comercialização das informações pessoais e financeiras roubadas."
        ),
        "acoes": [
            "Alterar imediatamente todas as senhas comprometidas (rede social, e-mail, bancos) e ativar Autenticação de Dois Fatores (2FA).",
            "Bloquear o remetente e denunciar a mensagem maliciosa na plataforma.",
            "Se dados bancários foram expostos, notificar o banco para cancelamento de cartões e monitoramento da conta.",
            "Salvar capturas de tela da mensagem original e do link malicioso recebido.",
            "Registrar B.O. em delegacia especializada para proteção legal em caso de uso indevido do nome (falsidade ideológica).",
        ],
    },

    # ── 5. RELACIONAMENTO ROMÂNTICO ───────────────────────────────────────────
    "Golpes Baseados Em Relacionamento": {
        "definicao": (
            "Manipulação psicológica e Engenharia Social para explorar vulnerabilidade emocional, "
            "empatia e confiança da vítima. O estelionatário cria identidades falsas atraentes, "
            "estabelece vínculo afetivo intenso e acelerado, e então explora a vítima fabricando "
            "falsas crises para obter dinheiro ou induzindo compartilhamento de mídias íntimas "
            "para posterior chantagem."
        ),
        "modus_operandi": (
            "Perfil falso atraente → abordagem intensa e romântica → criação de vínculo emocional → "
            "fabricação de crise urgente (acidente, dívida, emergência médica) exigindo dinheiro; "
            "OU indução a envio de conteúdo íntimo → chantagem com ameaça de expor à rede de contatos."
        ),
        "leis": [
            {
                "nome": "Art. 171 do Código Penal (Estelionato)",
                "tipo": "crime patrimonial",
                "descricao": "Obtenção de vantagem ilícita por meio de fraude, enganando a vítima.",
                "aplicacao": "Simulação de vínculo afetivo para obter transferências financeiras.",
            },
            {
                "nome": "Lei nº 14.155/2021 (Fraude Eletrônica)",
                "tipo": "crime digital",
                "descricao": "Inclui fraudes realizadas por meios digitais com penas agravadas.",
                "aplicacao": "Romance scam via redes sociais, aplicativos de namoro.",
            },
            {
                "nome": "Art. 158 do Código Penal (Extorsão)",
                "tipo": "crime contra a pessoa e patrimônio",
                "descricao": "Obrigar alguém mediante ameaça a fazer algo para obter vantagem.",
                "aplicacao": "Chantagem com mídias íntimas, ameaça de expor conteúdo à rede de contatos.",
            },
            {
                "nome": "Art. 218-C do Código Penal (Divulgação de Conteúdo Íntimo)",
                "tipo": "crime contra a dignidade sexual",
                "descricao": "Criminaliza divulgação de conteúdo íntimo sem consentimento da vítima.",
                "aplicacao": "Revenge porn, vazamento de fotos/vídeos íntimos, chantagem com imagens.",
            },
            {
                "nome": "Lei Maria da Penha (Lei nº 11.340/2006)",
                "tipo": "proteção à mulher",
                "descricao": "Protege mulheres contra violência doméstica e familiar, incluindo violência digital.",
                "aplicacao": "Violência psicológica e coação contra mulheres em contexto de intimidade artificialmente construída.",
            },
        ],
        "analise": (
            "A base legal assenta-se no Estelionato (Art. 171) e na Fraude Eletrônica (Lei 14.155/2021), "
            "punindo a obtenção de vantagem ilícita mediante simulação de vínculo afetivo. Quando a "
            "manipulação evolui para chantagem com mídias íntimas, incide a Extorsão (Art. 158) e o "
            "Art. 218-C, que criminaliza o registro ou divulgação não autorizada de cenas de intimidade. "
            "Se a violência psicológica e coação ocorrerem contra mulheres em contexto de intimidade "
            "artificialmente construída, os tribunais podem aplicar a Lei Maria da Penha."
        ),
        "acoes": [
            "Cortar todo o contato imediatamente; bloquear e excluir o golpista de todas as redes sociais e aplicativos.",
            "Tirar capturas de tela do perfil do agressor, de todas as ameaças e do histórico de conversas antes de bloquear.",
            "Acionar a instituição financeira rapidamente se transferências já foram realizadas sob manipulação.",
            "Denunciar o perfil falso usando as ferramentas do Facebook.",
            "Registrar B.O. na delegacia de crimes cibernéticos — especialmente crucial em casos de extorsão com imagens íntimas.",
        ],
    },

    # ── 6. SEGURO ─────────────────────────────────────────────────────────────
    "Seguro": {
        "definicao": "Conteúdo que não apresenta indícios de engenharia social, fraude ou intenção maliciosa.",
        "modus_operandi": "Não aplicável.",
        "leis": [],
        "analise": "Não é considerado crime. Nenhuma base legal aplicável.",
        "acoes": ["Nenhuma ação necessária."],
    },
}


# ── FUNÇÕES AUXILIARES ────────────────────────────────────────────────────────

def montar_contexto(categoria: str) -> str:
    """
    Monta o bloco de contexto RAG para uma categoria específica.
    Esse texto é injetado no prompt enviado à OpenAI.
    """
    if categoria not in BASE_CONHECIMENTO:
        return "Categoria não reconhecida. Sem base de conhecimento disponível."

    ctx = BASE_CONHECIMENTO[categoria]

    linhas = [
        f"CATEGORIA IDENTIFICADA: {categoria}",
        "",
        "DEFINIÇÃO:",
        ctx["definicao"],
        "",
        "MODUS OPERANDI:",
        ctx["modus_operandi"],
        "",
        "LEGISLAÇÃO APLICÁVEL:",
    ]

    for lei in ctx["leis"]:
        linhas += [
            f"  • {lei['nome']}",
            f"    Tipo: {lei['tipo']}",
            f"    Descrição: {lei['descricao']}",
            f"    Aplicação neste caso: {lei['aplicacao']}",
            "",
        ]

    linhas += [
        "ANÁLISE JURÍDICA CONSOLIDADA:",
        ctx["analise"],
        "",
        "AÇÕES RECOMENDADAS À VÍTIMA:",
    ]

    for i, acao in enumerate(ctx["acoes"], 1):
        linhas.append(f"  {i}. {acao}")

    return "\n".join(linhas)


def montar_prompt(mensagem: str, categoria: str, score: float) -> list[dict]:
    """
    Monta a lista de mensagens no formato da OpenAI Chat Completions API.
    Inclui o contexto RAG já recuperado e instrui o modelo a gerar
    Motivo, Base_Legal e Acoes_Recomendadas no formato JSON estrito.

    Args:
        mensagem  : texto original analisado
        categoria : categoria predita pelo BERTimbau
        score     : score de confiança do BERTimbau (0.0 a 1.0)

    Returns:
        Lista de dicts no formato [{role, content}] para a OpenAI API.
    """
    contexto = montar_contexto(categoria)

    confianca_str = (
        "ALTA (≥ 0,85)"      if score >= 0.85 else
        "MODERADA (0,60–0,84)" if score >= 0.60 else
        "BAIXA (< 0,60)"
    )

    system_prompt = """Você é um especialista em Cibersegurança e Direito Digital brasileiro.

Sua função é receber um texto já classificado por um modelo de machine learning e produzir uma resposta estruturada que justifica e enriquece essa classificação para alertar e orientar a vítima.

PREMISSA FUNDAMENTAL — CATEGORIA É VERDADE ABSOLUTA:
A categoria informada foi definida pelo modelo BERTimbau e deve ser tratada como correta e imutável. Sua tarefa NÃO é avaliar se a classificação está certa — é explicar POR QUE o texto se enquadra nessa categoria e quais consequências legais e ações decorrem disso. Nunca questione, contradiga ou ignore a categoria recebida.

PRINCÍPIO CENTRAL — BASE_LEGAL:
Prefira o falso negativo ao falso positivo. Só cite uma lei se houver evidência explícita e inequívoca no texto de que aquele dispositivo legal está sendo infringido. Dúvida = campo vazio.

REGRAS OBRIGATÓRIAS:
1. Use EXCLUSIVAMENTE as informações da BASE DE CONHECIMENTO fornecida. Não invente leis, artigos ou ações que não estejam no contexto.
2. O campo "Motivo" deve explicar, considerando que a categoria JÁ ESTÁ DEFINIDA, quais elementos do texto confirmam e ilustram esse enquadramento — cite trechos ou características concretas observadas. Nunca use o Motivo para sugerir que o texto poderia ser outra categoria ou que a classificação pode estar errada.
3. O campo "Base_Legal" deve listar SOMENTE as leis cujos elementos configuradores estejam explicitamente presentes no texto analisado. Não cite uma lei apenas porque ela consta na base de conhecimento da categoria — a lei só deve aparecer se o texto contiver evidência direta e inequívoca de que aquele dispositivo está sendo infringido. Exemplos de limiar mínimo exigido: Art. 307 (Falsa Identidade) exige impersonação explícita de uma pessoa ou instituição real; Art. 158 (Extorsão) exige ameaça explícita; Arts. 138-140 exigem atribuição de fato falso ou ofensa a pessoa identificável; LGPD exige coleta ou uso indevido de dados pessoais identificável no texto; Lei Carolina Dieckmann exige indício de invasão de dispositivo ou instalação de malware. Na dúvida sobre qualquer lei, não a cite.
4. FORMATO DE Base_Legal: copie os nomes das leis EXATAMENTE como aparecem nos marcadores "•" da seção LEGISLAÇÃO APLICÁVEL da base de conhecimento, separados por ponto e vírgula. Não abrevie, não parafraseie, não adicione texto explicativo. Exemplo correto: "Art. 171 do Código Penal (Estelionato); Lei nº 14.155/2021 (Fraude Eletrônica)". Se nenhuma lei se aplicar, retorne "".
5. O campo "Acoes_Recomendadas" deve seguir a ordem de prioridade da base de conhecimento, adaptando o texto ao contexto específico da mensagem.
6. Se a categoria for "Seguro", retorne o JSON com campos vazios e Acoes_Recomendadas = "Verifique a informação em fontes confiáveis antes de compartilhar."
7. Responda EXCLUSIVAMENTE com o JSON abaixo, sem texto adicional, markdown ou explicações fora do JSON.
8. Se o texto não contiver elementos que caracterizem claramente uma conduta ilícita, retorne "Base_Legal" vazio (""). Se apenas alguns elementos estiverem presentes, cite somente as leis com evidência direta no texto — nunca cite todas as leis da categoria por precaução."""

    user_prompt = f"""BASE DE CONHECIMENTO:
{contexto}

---

TEXTO ANALISADO:
\"\"\"{mensagem}\"\"\"

CATEGORIA DEFINIDA PELO MODELO (trate como verdade — não questione):
  Categoria  : {categoria}
  Confiança  : {score:.0%} ({confianca_str})

---

Com base EXCLUSIVAMENTE na BASE DE CONHECIMENTO acima, e assumindo que a categoria "{categoria}" está correta, gere o JSON abaixo:

{{
  "Categoria": "{categoria}",
  "Motivo": "<explique quais elementos do texto confirmam o enquadramento nesta categoria>",
  "Base_Legal": "<nomes exatos das leis aplicáveis, copiados dos marcadores • da base, separados por ponto e vírgula — ou vazio>",
  "Acoes_Recomendadas": "<liste as ações recomendadas adaptadas ao contexto desta mensagem>"
}}"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": user_prompt},
    ]
