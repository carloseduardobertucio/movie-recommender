from sqlalchemy.orm import Session
import numpy as np
from collections import defaultdict
from models import Movie, Rating, Viewing, Genre, Actor, Director

class MovieRecommender:
    def __init__(self, db: Session):
        self.db = db
        

    def get_user_ratings(self, user_id: int):
        return self.db.query(Rating).filter(Rating.user_id == user_id).all()


    def get_user_viewed_movies(self, user_id: int):
        return self.db.query(Viewing).filter(Viewing.user_id == user_id).all()


    def get_user_favorite_genres(self, user_id: int):
        user_ratings = self.get_user_ratings(user_id)
        
        genre_counts = defaultdict(int)
        genre_scores = defaultdict(float)
        
        for rating in user_ratings:
            movie = rating.movie
            for genre in movie.genres:
                genre_counts[genre.id] += 1
                genre_scores[genre.id] += rating.score
        
        # média de pontuação por gênero
        favorite_genres = {}
        for genre_id, count in genre_counts.items():
            favorite_genres[genre_id] = genre_scores[genre_id] / count

        return sorted(favorite_genres.items(), key=lambda x: x[1], reverse=True)

    def get_user_favorite_directors(self, user_id: int):
        user_ratings = self.get_user_ratings(user_id)
        
        director_counts = defaultdict(int)
        director_scores = defaultdict(float)
        
        for rating in user_ratings:
            movie = rating.movie
            director_id = movie.director_id
            director_counts[director_id] += 1
            director_scores[director_id] += rating.score
        
        # média de pontuação por diretor
        favorite_directors = {}
        for director_id, count in director_counts.items():
            favorite_directors[director_id] = director_scores[director_id] / count
            
        # diretores por pontuação média
        return sorted(favorite_directors.items(), key=lambda x: x[1], reverse=True)

    def get_user_favorite_actors(self, user_id: int):
        user_ratings = self.get_user_ratings(user_id)
        
        actor_counts = defaultdict(int)
        actor_scores = defaultdict(float)
        
        for rating in user_ratings:
            movie = rating.movie
            for actor in movie.actors:
                actor_counts[actor.id] += 1
                actor_scores[actor.id] += rating.score
        
        # média de pontuação por ator
        favorite_actors = {}
        for actor_id, count in actor_counts.items():
            favorite_actors[actor_id] = actor_scores[actor_id] / count
            
        return sorted(favorite_actors.items(), key=lambda x: x[1], reverse=True)

    def calculate_movie_similarity(self, movie_id, user_preferences):
        movie = self.db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            return 0
        
        score = 0
        
        # pontuação gêneros
        for genre in movie.genres:
            for genre_id, genre_score in user_preferences['genres']:
                if genre.id == genre_id:
                    score += genre_score
        
        # pontuação diretor
        for director_id, director_score in user_preferences['directors']:
            if movie.director_id == director_id:
                score += director_score * 2 
        
        # pontuação atores
        actor_ids = [actor.id for actor in movie.actors]
        for actor_id, actor_score in user_preferences['actors']:
            if actor_id in actor_ids:
                score += actor_score
        
        return score

    def get_recommendations(self, user_id: int, limit: int = 10):
        # filmes que o usuário já assistiu
        viewed_movies = self.get_user_viewed_movies(user_id)
        viewed_movie_ids = [viewing.movie_id for viewing in viewed_movies]
        
        # preferências do usuário
        user_preferences = {
            'genres': self.get_user_favorite_genres(user_id),
            'directors': self.get_user_favorite_directors(user_id),
            'actors': self.get_user_favorite_actors(user_id)
        }
        
        # todos os filmes que o usuário ainda não assistiu
        unseen_movies = self.db.query(Movie).filter(Movie.id.notin_(viewed_movie_ids)).all()
        
        movie_scores = []
        for movie in unseen_movies:
            similarity = self.calculate_movie_similarity(movie.id, user_preferences)
            movie_scores.append((movie, similarity))
        
        movie_scores.sort(key=lambda x: x[1], reverse=True)
        
        return movie_scores[:limit]
    
def recomendar_filmes(user_id: int, db: Session):
    recommender = MovieRecommender(db)
    return recommender.get_recommendations(user_id)

