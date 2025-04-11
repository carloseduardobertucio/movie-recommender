# 🎬 API de Recomendação de Filmes

Uma API RESTful construída com **FastAPI** e **SQLAlchemy**, que permite gerenciamento de filmes, gêneros, diretores, atores, usuários, avaliações e visualizações. A API também oferece recomendações personalizadas com base no histórico do usuário.

---

## 🚀 Funcionalidades

- CRUD de Filmes, Atores, Diretores e Gêneros  
- Criação de Usuários  
- Avaliação de filmes com notas  
- Registro de visualizações  
- Recomendações personalizadas  
- Seed automatizado com dados reais  

---

## 🧱 Estrutura do Projeto
📁 app/ ├── main.py ├── models.py ├── schemas.py ├── crud.py ├── database.py ├── seed_database.py
📁 static/ ├── index.html ├── style.css ├── script.js

---

## 👾 Execução 

## Clone o repositório:

git clone git@github.com:carloseduardobertucio/movie-recommender.git

---

## Crie um ambiente virtual:

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows


## Instale as dependências:

pip install -r requirements.txt


## Rode o seed (opcional, mas recomendado):
python seed_database.py


## Inicie a API:

uvicorn main:app --reload

Logo após, acesse: http://127.0.0.1:8000/

