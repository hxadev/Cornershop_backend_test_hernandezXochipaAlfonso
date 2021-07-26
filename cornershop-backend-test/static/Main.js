const Main = (function () {
  const initializeModule = () => {
    let container = $("body > div");

    container
      .find("table")
      .find("button[id='btnSlack']")
      .off("click")
      .on("click", function () {
        let row = $(this).parent().parent();
        let id = row.attr("data-id");
        if (id) {
          MainController.sendReminder({ id: id }).then(function (ev) {
              
          });   
        } else {
          alert("Dato invalido");
        }
      });
  };

  return {
    inicializar: function () {
      initializeModule();
    },
  };
})();

const MainController = (function () {
  return {
    sendReminder: function (data) {
      return $.post("/createReminerSlack", JSON.stringify(data)).fail(function (
        jqxhr,
        settings,
        ex
      ) {
        if ("responseJSON" in jqxhr) {
          let response = jqxhr.responseJSON;
          if ("message" in response) {
            alert(response.message);
          } else {
            alert("Ocurrio un error");
          }
        }
      });
    },
  };
})();

Main.inicializar();
