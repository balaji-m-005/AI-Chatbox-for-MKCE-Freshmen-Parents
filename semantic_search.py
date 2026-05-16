from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
faq_questions = []
faq_answers = []
faq_embeddings = None


def initialize_faq_embeddings(faqs):
    global faq_questions, faq_answers, faq_embeddings
    faq_questions = [faq.question for faq in faqs]
    faq_answers = [faq.answer for faq in faqs]
    if faq_questions:
        faq_embeddings = model.encode(faq_questions, convert_to_numpy=True)
    else:
        faq_embeddings = None


def search_semantic(query):
    global faq_embeddings, faq_answers
    if faq_embeddings is None or not faq_answers:
        return None, 0.0

    query_embedding = model.encode([query], convert_to_numpy=True)
    similarities = cosine_similarity(query_embedding, faq_embeddings)[0]

    best_index = int(np.argmax(similarities))
    best_score = float(similarities[best_index])

    if best_score <= 0.55:
        return None, best_score

    return faq_answers[best_index], best_score
