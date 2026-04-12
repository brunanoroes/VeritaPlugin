"""
Script executado antes de subir a API no Railway.
Baixa o modelo do HuggingFace se ainda não estiver na pasta local.
"""
import os
from huggingface_hub import snapshot_download

MODEL_DIR  = "modelo_bert"
REPO_ID    = "brunanoroes/veritaplugin-bert"

# Só baixa se o modelo ainda não estiver presente
if not os.path.exists(os.path.join(MODEL_DIR, "model.safetensors")):
    print(f"Baixando modelo de {REPO_ID}...")
    snapshot_download(repo_id=REPO_ID, local_dir=MODEL_DIR)
    print("Modelo baixado com sucesso!")
else:
    print("Modelo já presente, pulando download.")
