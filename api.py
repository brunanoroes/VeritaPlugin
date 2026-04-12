from dotenv import load_dotenv
load_dotenv()  # carrega o arquivo .env automaticamente

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from classificador_bert import classificar_mensagem
from pipeline_rag import analisar_mensagem

app = FastAPI(title="VeritaPlugin API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class FacebookContent(BaseModel):
    message: str
    api_key: str = ""


@app.post("/VeritaPlugin/CategorizeData")
async def categorize(body: FacebookContent):
    if not body.message or not body.message.strip():
        raise HTTPException(status_code=400, detail="Mensagem vazia.")

    chave = body.api_key or os.getenv("OPENAI_API_KEY", "")
    if not chave:
        raise HTTPException(status_code=401, detail="Chave da OpenAI não configurada.")

    categoria, score = classificar_mensagem(body.message)
    resultado = analisar_mensagem(body.message, categoria, score, api_key=chave)

    if resultado.get("Erro"):
        raise HTTPException(status_code=502, detail=resultado["Erro"])

    return {
        "categoria":       categoria,
        "risco":           round(score * 100),
        "explicacao":      resultado["Motivo"],
        "baseLegal":       resultado["Base_Legal"],
        "acaoRecomendada": resultado["Acoes_Recomendadas"],
    }


@app.get("/VeritaPlugin/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
