import {b} from "./generateProblem.js"
// Não está sendo utilizado no momento!!
function verificacao() {
  var qcampos = parseInt($("#quantidadeCampos").val());
  var qrestricoes = parseInt($("#quantidadeRestricoes").val());
  var tipoProblema = $("#solucao").val();

  if (
    qcampos <= 1 ||
    isNaN(qcampos) == true ||
    qrestricoes < 1 ||
    isNaN(qrestricoes) == true ||
    tipoProblema == null
  ) {
    if (tipoProblema == null) {
      alert("Escolha um método para solucionar o problema");
    } else {
      alert(
        "Por favor insira números positivos maiores que 1 para a quantidade de variáveis e valores maiores que 0 para as restrições"
      );
    }
  }else{
    oi();
  }
}

$("#btn").on("click", verificacao);
