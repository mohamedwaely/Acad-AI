from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from models.entities import PreProjects
from models.schemas import CheckProject
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(project: CheckProject, projects: list[PreProjects]) -> list[tuple[int, float]]:
    proj_txt = f"{project.title} {project.description}"
    projs_txt = [f"{pro.title} {pro.description}" for pro in projects]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([proj_txt] + projs_txt)
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    
    return [(i, score) for i, score in enumerate(similarity_matrix[0])]

def check_similarity(project: CheckProject, db: Session) -> dict:
    cur_date = datetime.now()
    cur_month = cur_date.month
    cur_year = cur_date.year

    if cur_month in [10, 11, 12]:
        cur_year += 1
    
    projects = db.query(PreProjects).filter(PreProjects.year == cur_year).all()

    if not projects:
        try:
            new_proj = PreProjects(
                title=project.title,
                description=project.description,
                year=cur_year
            )
            db.add(new_proj)
            db.commit()
            db.refresh(new_proj)
            return {"message": "Project added successfully", "similarity": "Your is the first project in the year"}
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error in adding project")
    else:
        all_similarities = calculate_similarity(project, projects)
        
        similar_projects = [(i, score) for i, score in all_similarities if score > 0.5]

        if similar_projects:
            sim_projs = [
                {"title": projects[i].title, "similarity score": f"{score:.2f}"} for i, score in similar_projects
            ]
            return {
                "message": "There are projects similar to your idea due to DMU policy", 
                "similar projects": sim_projs
            }
        else:
            try:
                new_proj = PreProjects(
                    title=project.title,
                    description=project.description,
                    year=cur_year
                )
                db.add(new_proj)
                db.commit()
                db.refresh(new_proj)

                all_projs = [
                    {"title": projects[i].title, "similarity score": f"{score:.2f}"} for i, score in all_similarities
                ]
                return {
                    "message": "Congrats, Your project added successfully",
                    "similarity scores": all_projs,
                }
            except Exception as e:
                raise HTTPException(status_code=400, detail="Error in adding project")