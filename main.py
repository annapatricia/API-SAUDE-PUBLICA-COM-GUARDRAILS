from fastapi import FastAPI, HTTPException         #isto é o guardrail
from pydantic import BaseModel, validator          #isto é o guardrail
from fastapi import FastAPI

app = FastAPI(title="API Saúde Pública")

#quadrils
PALAVRAS_PROIBIDAS = [
    "tiro", "arma", "bomba", "matar", "veneno",
    "explosivo", "suicídio", "assassinato"
]
def verificar_conteudo(texto: str):
    for palavra in PALAVRAS_PROIBIDAS:
        if palavra in texto.lower():
            raise HTTPException(
                status_code=400,
                detail="Conteúdo inválido ou fora do escopo médico"
            )
 #quadrils

#Modelo com guardrils
class Doenca(BaseModel):
    nome: str
    descricao: str
    sintomas: list[str]
    tratamento: str

    @validator("nome", "descricao", "tratamento")
    def validar_texto(cls, v):
        verificar_conteudo(v)
        return v
#Modelo com guardrils


#Base de dados simples
doencas = [
    {
        "id": 1,
        "nome": "Diabetes Mellitus",
        "descricao": "Doença crônica caracterizada por níveis elevados de glicose no sangue.",
        "sintomas": ["sede excessiva", "urinar frequentemente", "fadiga"],
        "tratamento": "Dieta, atividade física e insulina."
    }
]
#Base de dados simples



#endpoint (sempre por ultimos)
@app.get("/")
def home():
    return {"mensagem": "Sistema de regulação online"}

@app.get("/doencas")
def listar_doencas():
    return doencas

@app.get("/doencas/{nome_doenca}")
def buscar_doenca(nome_doenca: str):
    verificar_conteudo(nome_doenca)

    for d in doencas:
        if nome_doenca.lower() in d["nome"].lower():
            return d

    raise HTTPException(
        status_code=404,
        detail="Doença não encontrada"
    )
    
@app.post("/doencas")
def cadastrar_doenca(doenca: Doenca):
    novo_id = max(d["id"] for d in doencas) + 1 if doencas else 1
    nova_doenca = doenca.dict()
    nova_doenca["id"] = novo_id
    doencas.append(nova_doenca)
    return {
        "mensagem": "Doença cadastrada com sucesso",
        "doenca": nova_doenca
    }

#endpoint (sempre por ultimos)



