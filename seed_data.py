import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session

# create table
models.Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    try:
        if db.query(models.Movie).count() > 0:
            print("Banco de dados já possui dados. Pulando seed.")
            return
        
        # add genrers
        generos = [
            models.Genre(name="Ação"),
            models.Genre(name="Aventura"),
            models.Genre(name="Comédia"),
            models.Genre(name="Drama"),
            models.Genre(name="Ficção Científica"),
            models.Genre(name="Terror"),
            models.Genre(name="Romance"),
            models.Genre(name="Animação"),
            models.Genre(name="Documentário"),
            models.Genre(name="Suspense")
        ]
        
        for genero in generos:
            db.add(genero)
        db.commit()
        
        # add directors
        diretores = [
            models.Director(name="Christopher Nolan"),
            models.Director(name="Steven Spielberg"),
            models.Director(name="Martin Scorsese"),
            models.Director(name="Quentin Tarantino"),
            models.Director(name="James Cameron"),
            models.Director(name="Greta Gerwig"),
            models.Director(name="Taika Waititi")
        ]
        
        for diretor in diretores:
            db.add(diretor)
        db.commit()
        
        # add actors
        atores = [
            models.Actor(name="Leonardo DiCaprio"),
            models.Actor(name="Tom Hanks"),
            models.Actor(name="Scarlett Johansson"),
            models.Actor(name="Robert Downey Jr."),
            models.Actor(name="Jennifer Lawrence"),
            models.Actor(name="Brad Pitt"),
            models.Actor(name="Meryl Streep"),
            models.Actor(name="Denzel Washington"),
            models.Actor(name="Emma Stone"),
            models.Actor(name="Chris Evans")
        ]
        
        for ator in atores:
            db.add(ator)
        db.commit()
        

        generos = db.query(models.Genre).all()
        diretores = db.query(models.Director).all()
        atores = db.query(models.Actor).all()
        
        # add movies
        filmes = [
            {
                "title": "Interestelar",
                "description": "Um grupo de astronautas viaja através de um buraco de minhoca em busca de um novo lar para a humanidade.",
                "release_year": 2014,
                "director_id": diretores[0].id,  
                "actors": [atores[0], atores[4]], 
                "genres": [generos[4], generos[3]] 
            },
            {
                "title": "O Resgate do Soldado Ryan",
                "description": "Durante a Segunda Guerra Mundial, um grupo de soldados é enviado para salvar um paraquedista cujos irmãos morreram em combate.",
                "release_year": 1998,
                "director_id": diretores[1].id, 
                "actors": [atores[1], atores[7]],  
                "genres": [generos[0], generos[3]]  
            },
            {
                "title": "Os Bons Companheiros",
                "description": "A história de Henry Hill e sua vida no crime, cobrindo sua relação com sua esposa e seus parceiros da máfia.",
                "release_year": 1990,
                "director_id": diretores[2].id,  
                "actors": [atores[5], atores[0]],  
                "genres": [generos[3], generos[9]]  
            },
            {
                "title": "Pulp Fiction",
                "description": "As vidas de dois assassinos, um boxeador, um gângster e sua esposa se entrelaçam em quatro histórias de violência e redenção.",
                "release_year": 1994,
                "director_id": diretores[3].id,  
                "actors": [atores[7], atores[5]],  
                "genres": [generos[3], generos[9]] 
            },
            {
                "title": "Avatar",
                "description": "Um militar paraplégico é enviado a Pandora numa missão única, mas fica dividido entre seguir suas ordens e proteger o mundo que sente ser sua casa.",
                "release_year": 2009,
                "director_id": diretores[4].id,  
                "actors": [atores[2], atores[3]],  
                "genres": [generos[4], generos[1]]  
            },
            {
                "title": "Lady Bird",
                "description": "No último ano do ensino médio, uma jovem tenta se equilibrar entre sonhos e realidades enquanto lida com seu relacionamento complicado com a mãe.",
                "release_year": 2017,
                "director_id": diretores[5].id,  
                "actors": [atores[8], atores[6]], 
                "genres": [generos[3], generos[2]] 
            },
            {
                "title": "Thor: Ragnarok",
                "description": "Thor se encontra preso do outro lado do universo e precisa correr contra o tempo para voltar a Asgard e impedir o Ragnarok.",
                "release_year": 2017,
                "director_id": diretores[6].id, 
                "actors": [atores[9], atores[3]],
                "genres": [generos[0], generos[1], generos[2]]  
            },
            {
                "title": "A Origem",
                "description": "Um ladrão que rouba segredos corporativos através do uso da tecnologia de compartilhamento de sonhos recebe a tarefa inversa de plantar uma ideia na mente de um CEO.",
                "release_year": 2010,
                "director_id": diretores[0].id,  
                "actors": [atores[0], atores[5]],  
                "genres": [generos[4], generos[0], generos[9]]  
            },
            {
                "title": "O Lobo de Wall Street",
                "description": "Baseado na história real de Jordan Belfort, desde sua ascensão como um corretor de bolsa rico até sua queda envolvendo crime e corrupção.",
                "release_year": 2013,
                "director_id": diretores[2].id, 
                "actors": [atores[0], atores[4]],  
                "genres": [generos[3], generos[2]]  
            },
            {
                "title": "Os Vingadores",
                "description": "Os heróis mais poderosos da Terra devem se unir e aprender a lutar em equipe para impedir que Loki e seu exército alienígena escravizem a humanidade.",
                "release_year": 2012,
                "director_id": diretores[1].id,  
                "actors": [atores[3], atores[9], atores[2]],  
                "genres": [generos[0], generos[4], generos[1]]  
            }
        ]
        
        for filme_data in filmes:
            atores_list = filme_data.pop("actors")
            generos_list = filme_data.pop("genres")
            
            filme = models.Movie(**filme_data)
            filme.actors = atores_list
            filme.genres = generos_list
            
            db.add(filme)
        db.commit()
        
        # add users
        usuarios = [
            models.User(username="usuario1"),
            models.User(username="usuario2"),
            models.User(username="usuario3")
        ]
        
        for usuario in usuarios:
            db.add(usuario)
        db.commit()
        

        db.add(models.Rating(user_id=1, movie_id=1, score=5.0))  
        db.add(models.Rating(user_id=1, movie_id=8, score=4.5))  
        db.add(models.Rating(user_id=1, movie_id=5, score=4.0))  
        db.add(models.Viewing(user_id=1, movie_id=1))
        db.add(models.Viewing(user_id=1, movie_id=8))
        db.add(models.Viewing(user_id=1, movie_id=5))
        

        db.add(models.Rating(user_id=2, movie_id=3, score=5.0))  
        db.add(models.Rating(user_id=2, movie_id=9, score=4.5))  
        db.add(models.Rating(user_id=2, movie_id=6, score=4.0))  
        db.add(models.Viewing(user_id=2, movie_id=3))
        db.add(models.Viewing(user_id=2, movie_id=9))
        db.add(models.Viewing(user_id=2, movie_id=6))
        

        db.add(models.Rating(user_id=3, movie_id=10, score=5.0))  
        db.add(models.Rating(user_id=3, movie_id=7, score=4.5))  
        db.add(models.Rating(user_id=3, movie_id=2, score=4.0))  
        db.add(models.Viewing(user_id=3, movie_id=7))
        db.add(models.Viewing(user_id=3, movie_id=2))
        
        db.commit()
        
        print("Banco de dados populado com sucesso!")
    
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()