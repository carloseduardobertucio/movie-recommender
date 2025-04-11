from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import engine, get_db
import schemas as schemas
from recommender import MovieRecommender
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


# tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BisoFlix - Sistema de Recomendação de Filmes",
    description="API para recomendar filmes com base no histórico de visualização e preferências dos usuários",
    version="1.0.0"
)


@app.get("/", include_in_schema=False)
def serve_index():
    return FileResponse("static/index.html")


@app.get("/filmes", response_model=List[schemas.Movie], tags=["Filmes"])
def get_all_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = db.query(models.Movie).offset(skip).limit(limit).all()

    for movie in movies:
        ratings = [rating.score for rating in movie.ratings]
        movie.average_rating = sum(ratings) / len(ratings) if ratings else None
    
    return movies


@app.get("/filmes/{filme_id}", response_model=schemas.Movie, tags=["Filmes"])
def get_movie(filme_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == filme_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Filme não encontrado")

    ratings = [rating.score for rating in movie.ratings]
    movie.average_rating = sum(ratings) / len(ratings) if ratings else None
    
    return movie


@app.get("/filmes/{usuario_id}/recomendacoes", tags=["Recomendações"])
def get_recommendations(usuario_id: int, limit: int = 10, db: Session = Depends(get_db)):

    # o usuário existe?
    user = db.query(models.User).filter(models.User.id == usuario_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    recommender = MovieRecommender(db)
    recommendations = recommender.get_recommendations(usuario_id, limit)

    result = []
    for movie, similarity_score in recommendations:
        ratings = [rating.score for rating in movie.ratings]
        movie.average_rating = sum(ratings) / len(ratings) if ratings else None
        
        result.append({
            "movie": movie,
            "similarity_score": similarity_score
        })
    
    return result


@app.post("/usuarios", response_model=schemas.User, tags=["Usuários"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # o usuário já existe ?
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username já registrado")
    
    # Criar novo usuário
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/avaliacoes", response_model=schemas.Rating, tags=["Avaliações"])
def create_rating(rating: schemas.RatingCreate, db: Session = Depends(get_db)):
    # o usuário existe?
    user = db.query(models.User).filter(models.User.id == rating.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # o filme existe ?
    movie = db.query(models.Movie).filter(models.Movie.id == rating.movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    
    # já existe uma avaliação?
    existing_rating = db.query(models.Rating).filter(
        models.Rating.user_id == rating.user_id,
        models.Rating.movie_id == rating.movie_id
    ).first()
    
    if existing_rating:
        existing_rating.score = rating.score
        db.commit()
        db.refresh(existing_rating)
        return existing_rating
    else:
        db_rating = models.Rating(**rating.dict())
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating


@app.post("/visualizacoes", tags=["Visualizações"])
def record_viewing(viewing: schemas.ViewingCreate, db: Session = Depends(get_db)):
    # o usuário existe?
    user = db.query(models.User).filter(models.User.id == viewing.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # o filme existe?
    movie = db.query(models.Movie).filter(models.Movie.id == viewing.movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    
    # já existe um registro de visualização?
    existing_viewing = db.query(models.Viewing).filter(
        models.Viewing.user_id == viewing.user_id,
        models.Viewing.movie_id == viewing.movie_id
    ).first()
    
    if existing_viewing:
        return {"message": "Visualização já registrada"}
    else:
        db_viewing = models.Viewing(**viewing.dict())
        db.add(db_viewing)
        db.commit()
        db.refresh(db_viewing)
        return {"message": "Visualização registrada com sucesso"}

app.mount("/static", StaticFiles(directory="static"), name="static")