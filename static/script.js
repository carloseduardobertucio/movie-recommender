const API_URL = "http://127.0.0.1:8000";

async function criarUsuario() {
  const username = document.getElementById("username").value;
  const res = await fetch(`${API_URL}/usuarios`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username })
  });

  const data = await res.json();
  alert(data.username ? `Usuário criado: ${data.username}` : data.detail);
}

async function carregarFilmes() {
  const res = await fetch(`${API_URL}/filmes`);
  const filmes = await res.json();
  const lista = document.getElementById("lista-filmes");
  lista.innerHTML = "";

  filmes.forEach(filme => {
    const li = document.createElement("li");
    li.innerText = `${filme.id}: ${filme.title} (${filme.release_year})`;
    lista.appendChild(li);
  });
}

async function avaliarFilme() {
  const userId = +document.getElementById("userIdRating").value;
  const movieId = +document.getElementById("movieIdRating").value;
  const score = +document.getElementById("score").value;

  const res = await fetch(`${API_URL}/avaliacoes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, movie_id: movieId, score })
  });

  const data = await res.json();
  alert(data.id ? `Avaliação registrada.` : data.detail);
}

async function verRecomendacoes() {
  const userId = document.getElementById("userIdRecom").value;
  const res = await fetch(`${API_URL}/filmes/${userId}/recomendacoes`);
  const lista = await res.json();
  const ul = document.getElementById("lista-recomendacoes");
  ul.innerHTML = "";

  lista.forEach(rec => {
    const li = document.createElement("li");
    li.innerText = `${rec.movie.title} - Nota Média: ${rec.movie.average_rating?.toFixed(1) ?? 'N/A'}`;
    ul.appendChild(li);
  });
}
