from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(project, projects: list):
    proj_txt=f"{project.title} {project.description}"
    projs_txt = [f"{pro.title} {pro.description}" for pro in projects]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([proj_txt] + projs_txt)
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

    all_similarities = [(i, score) for i, score in enumerate(similarity_matrix[0])]

    return all_similarities