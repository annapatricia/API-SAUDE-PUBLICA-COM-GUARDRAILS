from fastapi import FastAPI
app = FastAPI(title="API Saúde Pública")
@app.get("/")
def home():
    return {"mensagem": "Sistema de regulação online"}
