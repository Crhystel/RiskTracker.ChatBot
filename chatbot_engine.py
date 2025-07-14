import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class ChatbotEngine:
    def __init__(self, faqs_path, model_name='all-MiniLM-L6-v2'):

        print("Iniciando motor del chatbot...")
        self.faqs = self._load_faqs(faqs_path)
        # Extraemos solo las preguntas para generar los embeddings
        questions = [item['question'] for item in self.faqs]
        
        print(f"Cargando el modelo '{model_name}'... (Esto puede tardar un poco la primera vez)")
        self.model = SentenceTransformer(model_name)
        
        print("Generando embeddings para la base de conocimiento...")
        self.question_embeddings = self.model.encode(questions, convert_to_tensor=False)
        print("Motor del chatbot listo.")

    def _load_faqs(self, file_path):

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def find_best_answer(self, user_question, similarity_threshold=0.6):

        # Genera el embedding para la pregunta del usuario
        user_embedding = self.model.encode([user_question], convert_to_tensor=False)

        # Calcula las similitudes
        similarities = cosine_similarity(user_embedding, self.question_embeddings)

        # Encuentra el índice y el valor de la similitud más alta
        best_match_index = np.argmax(similarities)
        best_match_score = similarities[0][best_match_index]
        
        print(f"Pregunta del usuario: '{user_question}'")
        print(f"Mejor coincidencia: '{self.faqs[best_match_index]['question']}' (Puntuación: {best_match_score:.4f})")

        # Compara 
        if best_match_score >= similarity_threshold:
            return self.faqs[best_match_index]['answer']
        else:
            return "Lo siento, no he podido encontrar una respuesta para tu pregunta. ¿Puedes intentar reformularla?"

if __name__ == '__main__':
    engine = ChatbotEngine(faqs_path='faqs.json')
    
    # Prueba
    user_query = "¿de qué se encarga el dueño del producto?"
    answer = engine.find_best_answer(user_query)
    print(f"\nRespuesta: {answer}")