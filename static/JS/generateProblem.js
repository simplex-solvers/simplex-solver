function gerarCampos() { // Chama as demais funções
  gerarCFuncaoObjetivo();
  gerarRestricoes();
  disableButton();
}

function gerarCFuncaoObjetivo() {
  //Pega a quantidade de de campos que será gerado através do #id
  var qtdeCampos = parseInt($("#quantidadeCampos").val());

  // Limpa o conteúdo anterior se houver algum
  $("#container").empty();

  var tituloFO = $("<h4>").text("Função");
  $("#container").append(tituloFO);

  //Loop responsável por gerar as labels e os inputs
  for (var i = 0; i < qtdeCampos; i++) {
    //cria o elemento label
    var label = $("<label>").attr("for", "campo" + i);

    //Condição no qual o ultimo campo da variavel criada não receba o caractere '+'
    if (i < qtdeCampos - 1) {
      label.text("x" + (i + 1) + " + ");
    } else {
      label.text("x" + (i + 1) + " ");
    }

    // Cria o campo de entrada de texto
    var input = $("<input>")
      .attr("type", "number")
      .attr("step","0.01")
      .attr("id", "campo" + i)
      .attr("name", "campo[]")
      .attr("class", "campo");

    // Adiciona a label e o campo ao contêiner
    $("#container").append(input);
    $("#container").append(label);
  }
  select2(); //Select para definir Maximo e Minimo

  $("<br>").appendTo("#container");// Quebra de linha
}

function gerarRestricoes() {
  let qtdeCampos = parseInt($("#quantidadeCampos").val());
  let quantidadeRestricoes = parseInt($("#quantidadeRestricoes").val());

  tituloRES = $("<h4>").text("Restrições");
  $("#container").append(tituloRES);

  for (let j = 0; j < quantidadeRestricoes; j++) {
    for (let i = 0; i < qtdeCampos; i++) {
      let label = $("<label>").attr("for", "campoR" + i);
      let input = $("<input>")
        .attr("type", "number")
        .attr("step","0.01")
        .attr("id", "campoR" + i + j)
        .attr("name","campoR[]")
        .attr("class", "campo");

      if (i < qtdeCampos - 1) {
        label.text("x" + (i + 1) + " + ");
      } else {
        label.text("x" + (i + 1) + " ");
      }

      input.appendTo("#container");
      label.appendTo("#container");
    }

    gerarSelect(j);

    let inputR = $("<input>")
      .attr("type", "number")
      .attr("step","0.01")
      .attr("id", "resp" + j)
      .attr("name","resp[]")
      .attr("class","campo");

    inputR.appendTo("#container");

    $("<br>").appendTo("#container");
  }
}

function addOption(select, value, text) {// Adiciona o nome da opção e o valor ao select
  select.append(new Option(text, value));
}

function gerarSelect(i) { // Select para os sinais das restrições <=, =, >=
  let label = $("<label>").text("   ");
  let select = $("<select>")
  .attr("id", "constr" + i)
  .attr("name","constr[]").attr("class", "constraints");

  select.appendTo("#container");
  label.appendTo("#container");

  select.change(function () {
    // Ações a serem tomadas quando o valor do campo selecionado mudar
  });

  addOption(select, "<=", "≤");
  addOption(select, "=", "=");
  addOption(select, ">=", "≥");
}

function select2() { // Select para o tipo de problema Maximização / Minimização
  let label2 = $("<label>").text(" ");
  let select2 = $("<select>")
  .attr("id", "tipo_problema")
  .attr("name","tipoProblema")
  .attr("class", "select tall");

  select2.appendTo("#container");
  label2.appendTo("#container");

  select2.change(function () {
    // Ações a serem tomadas quando o valor do campo selecionado mudar
  });

  addOption(select2, "max", "Maximizar");
  addOption(select2, "min", "Minimizar");
}

function verificacao() { // Responsável por impedir que dados iconsistentes buguem o sistema
  var qcampos = parseInt($("#quantidadeCampos").val());
  var qrestricoes = parseInt($("#quantidadeRestricoes").val());
  var tipoProblema = $("#solucao").val();

  if ( // Verifica se algum campo da função objetivo irá receber um valor inferior a 2 para as variáveis
    qcampos <= 1 || // e a quntidade de restrições seja infeior a 1
    isNaN(qcampos) == true ||
    qrestricoes < 1 ||
    isNaN(qrestricoes) == true ||
    tipoProblema == null
  ) {
    if (tipoProblema == null) { // Caso o usuário não selecione um tipo de solução
      alert("Escolha um método para solucionar o problema");// Mensagem
    } else {
      alert(
        "Por favor insira números positivos maiores que 1 para a quantidade de variáveis e valores maiores que 0 para as restrições" // Mensagem
      );
    }
  } else {
    gerarCampos();
  }
}

function disableButton() {// Responsável por desabilitar o botão de solução gráfica caso a opção não esteja selecionada
  var qcampos = parseInt($("#quantidadeCampos").val());// Ou a quantidade de variáveis seja superior a 2
  if (qcampos > 2) {
    $('#solucao option[value="graph"]').prop("disabled", true); // Desabilita o botão
    $("#solucao").val("primal");// Seleciona a solução primal no lugar
  } else {
    $('#solucao option[value="graph"]').prop("disabled", false); // Habilita o botão
  }

  if (qcampos > 2 || $("#solucao").val() != "graph") {
    $("#btnsolgraphic").addClass("disable").removeClass("enable"); //desabilitar botão para solução gráfica se o número de variáveis for maior que dois
  } else {
    $("#btnsolgraphic").removeClass("disable").addClass("enable"); //habilitar botão para solução gráfica se o número de variáveis for maenor ou igual a dois
  }
}

$("#btn").on("click", verificacao);
