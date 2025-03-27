from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse

from app import auth, models, schemas, security
from app.db import get_db
from app.models import User, Admin
import os
from datetime import datetime
from controllers.similarity_scores import calculate_similarity

def check_similarity(project: schemas.checkProject, db: Session = Depends(get_db)):
    cur_date=datetime.now()
    cur_month=cur_date.month
    cur_year=cur_date.year

    if cur_month in [10, 11, 12]:
        cur_year+=1
    
    projects = db.query(models.PreProjects).filter(models.PreProjects.year==cur_year).all()

    if not projects:
        try:
            new_proj=models.PreProjects(
                title=project.title,
                description=project.description,
                year=cur_year
            )
            db.add(new_proj)
            db.commit()
            db.refresh(new_proj)
            return {"message": "Project added successfully", "similarity": "Your is the first project in the year"}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="Error in adding project")

    else:
        all_similarities=calculate_similarity(project, projects)
        
        similar_projects=[(i, score) for i, score in all_similarities if score > 0.5]

        if similar_projects:
            sim_projs=[
                {"title": projects[i].title, "similarity score": f"{score:.2f}"} for i, score in similar_projects
            ]
            return {
                    "message": "There are projects similar to your idea due to DMU policy", 
                    "similar projects": sim_projs
                }

        else:
            try:
                new_proj=models.PreProjects(
                    title=project.title,
                    description=project.description,
                    year=cur_year
                )
                db.add(new_proj)
                db.commit()
                db.refresh(new_proj)

                all_projs=[
                    {"title": projects[i].title, "similarity score": f"{score:.2f}"} for i, score in all_similarities
                ]
                return {
                    "message": "Congrats, Your project added successfully",
                    "similarity scores": all_projs,
                }
            except Exception as e:
                print(e)
                raise HTTPException(status_code=400, detail="Error in adding project")
