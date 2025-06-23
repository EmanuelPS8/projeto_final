window.onload = Inicio;
const caminho = "img/";
const prefixo = "img";
const extensao = ".jpg";
var cont = 0;

// Animação de fade-in ao carregar a página
window.addEventListener("DOMContentLoaded", () => {
  document.body.classList.add("fade-in-page");
});

var lista = [
  { img: 1, titulo: "Imagem 1", descricao: "Descrição da Imagem 1" },
  { img: 2, titulo: "Imagem 2", descricao: "Descrição da Imagem 2" },
  { img: 3, titulo: "Imagem 3", descricao: "Descrição da Imagem 3" },
];

var botaoVoltar = document.getElementById("btnVoltar");
var botaoAvancar = document.getElementById("btnAvancar");
var moldura = document.getElementById("moldura");

function Inicio() {
  botaoAvancar.onclick = Avancar;
  botaoVoltar.onclick = Voltar;
  Atualizar();
}

function Avancar() {
  cont = (cont + 1) % lista.length;
  Atualizar();
}

function Voltar() {
  cont = (cont - 1 + lista.length) % lista.length;
  Atualizar();
}

function Atualizar() {
  if (cont < lista.length) {
    moldura.src = caminho + prefixo + lista[cont].img + extensao;
  } else {
    alert("O Cont é maior que o número de elementos");
  }
}
