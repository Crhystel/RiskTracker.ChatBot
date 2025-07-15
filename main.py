from fastapi import FastAPI
from pydantic import BaseModel
from chatbot_engine import ChatbotEngine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CatBot API",
    version="1.0.0"
)
origins = [
    "https://localhost:7135",
    "http://localhost:5136",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)

# Inicializamos el motor del chatbot con las FAQs
engine = ChatbotEngine(faqs_path='faqs.json')

class Query(BaseModel):
    text: str

#Endpoint
@app.get("/", tags=["Status"])
def read_root():
    return {"status": "ok", "message": "Bienvenido a la API del Chatbot"}

#Endpoint principal
@app.post("/ask", tags=["Chatbot"])
def ask_question(query: Query):
    answer = engine.find_best_answer(query.text)
    return {"question": query.text, "answer": answer}
