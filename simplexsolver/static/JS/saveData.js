function salvarDados() {
  var qtdeCampos = parseInt($("#quantidadeCampos").val()); //num_of_var
  var qtdeRestricoes = parseInt($("#quantidadeRestricoes").val());
  var camposObjetivo = []; //c
  var restricoes = []; //A
  var resultados = []; //b
  var sinal = []; //constraints
  var tipoFuncao = $("#tipo_problema").val(); //problem_type
  var tipoSolucao = $("#solucao").val(); //problem_form

  // Pega os valores dos campos do objetivo
  for (var i = 0; i < qtdeCampos; i++) {
    camposObjetivo.push(parseFloat($("#campo" + i).val()));
  }

  // Pega os valores das restrições
  for (var j = 0; j < qtdeRestricoes; j++) {
    var restricao = [];
    for (var i = 0; i < qtdeCampos; i++) {
      restricao.push(parseFloat($("#campoR" + i + j).val()));
    }
    restricoes.push(restricao);
    resultados.push(parseFloat($("#resp" + j).val()));
  }

  for (var i = 0; i < qtdeRestricoes; i++) {
    // Pega o sinal das restrições
    sinal.push($("#constr" + i).val());
  }

  // Objeto JS com os dados do formulário
  var dados = {
    c: camposObjetivo,
    A: restricoes,
    b: resultados,
    problem_form: tipoSolucao,
    problem_type: tipoFuncao,
    constraints: sinal,
    num_of_var: qtdeCampos,
  };

  // Transforma O objeto JS em uma string JSON
  var json = JSON.stringify(dados);

  console.log(dados);

  // Envia os dados JSON para o Flask
  fetch(rota, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: json,
  })
      .then((response) => response.json()) // Representa a resposta a uma solicitação. Cria o JSON.
    .then((data) => console.log("Success:", data)) // Se ocorreu tudo bem exibe os dados
    .catch((error) => console.error("Error:", error)); // Mostra se houve algum erro
}

var rota = null; // Variável responsável por definir a rota de entrega do JSON

//$("#salv").on("click", salvarDados);
$("button").click(function () {// Função responsável por descobrir qual botão foi clicado através de seu Id e redirecionar para o link correspondente
  console.log(this.id);
  if (this.id == "btnsolgraphic") {
    rota = "/grafico";
    // Redireciona o botão para o link específico armazenado no atributo data-url
    window.location.href = $(this).data("url");
  } else if (this.id == "iterations") {
    rota = "/tabular";
    // Redireciona o botão para o link específico armazenado no atributo data-url
    window.location.href = $(this).data("url");
  }

  salvarDados();
});
