import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, BertForSequenceClassification

MODEL_PATH = "modelo_bert"

LABELS = {
    0: "Golpes Baseados Em Relacionamento",
    1: "Golpes de Ganho Financeiro Ilusório",
    2: "Ataques de Phishing e Roubo de Dados",
    3: "Fraudes em Lojas Virtuais Falsas",
    4: "Golpes de Desinformação Digital",
    5: "Seguro",
}

# Carregados uma vez quando o módulo é importado
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()


def classificar_mensagem(mensagem: str) -> tuple[str, float]:
    """
    Classifica uma mensagem usando o modelo BERTimbau treinado.

    Retorna:
        (categoria, score) — nome da categoria e confiança entre 0.0 e 1.0
    """
    inputs = tokenizer(
        mensagem,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True,
    )
    with torch.no_grad():
        logits = model(**inputs).logits

    probs = F.softmax(logits, dim=-1)[0]
    idx = int(probs.argmax().item())
    score = round(float(probs[idx].item()), 4)

    return LABELS[idx], score
