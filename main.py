from fastapi import FastAPI
from pydantic import BaseModel
from chatbot_engine import ChatbotEngine

app = FastAPI(
    title="CatBot API",
    version="1.0.0"
)
origins = [
    "https://localhost:7135", # Origen por defecto de Blazor en desarrollo
    "http://localhost:5136",
    # Añade aquí la URL de producción si la tienes
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todas las cabeceras
)

# Inicializamos el motor del chatbot con las FAQs
engine = ChatbotEngine(faqs_path='faqs.json')

# Definimos el modelo de datos para la pregunta que llegará en el request
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

# Para ejecutar localmente sin Docker:
# Abre una terminal y corre: uvicorn main:app --reload