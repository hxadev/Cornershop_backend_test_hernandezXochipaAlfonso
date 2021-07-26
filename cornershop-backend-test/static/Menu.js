const Menu = (function () {
  const initializeModule = () => {
    const container = $("#principalContainer");
    const table = $("#tablaComidasPedido");
    InitialActionsModule(container);

    $("button[id='btnGuardarMenu']")
      .off("click")
      .on("click", function () {
        MenuController.saveMenu(JsonObject.SaveMenu(container)).then(function (
          res
        ) {
          if (res.status === "ok") {
            let data = JSON.parse(res.data)[0];
            container.find("input[id='id']").val(data.pk);
            container.find("#contenidoPlatillos").show();
            $(this).hide();
          }
        });
      });

    $("button[id='btnGuardarPlatillo']")
      .off("click")
      .on("click", function () {
        MenuController.saveMeal(JsonObject.SaveMeal(container)).then(function (
          res
        ) {
          if (res.status === "ok") {
            let data = JSON.parse(res.data)[0];

            let contenidoTabla = $("#contenidoListadoPlatillos").show();
            contenidoTabla.find("table").find("tbody").append(`
              <tr data-id="${data.pk}">
                <td>${data.fields.key}</td>
                <td>${data.fields.description}</td>
                <td><button id="eliminar" class="btn btn-danger" data-id="${data.pk}">Eliminar</button></td>
              </tr>
            `);

            container.find("input[id='platilloNombre']").val("");
            container.find("textarea[id='platilloDescripcion']").val("");
            if ($("#tablaComidasPedido").find("tbody").find("tr").length > 1) {
              let dateInput = new Date($("#fechaMenu").val());
              let today = new Date();
              let todayDate = new Date(
                `${today.getFullYear()}-${today.getMonth()}-${today.getDay()}`
              );

              $("#btnSendMenu").show();
              if (dateInput === todayDate) {
                $("#btnSendMenu").text("Enviar Menu =)");
              } else if (dateInput >= todayDate) {
                $("#btnSendMenu").text("Guardar Menu");
              }
            }
          }
        });
      });

    $("button[id='btnSendMenu']")
      .off("click")
      .on("click", function () {
        MenuController.sendMenu(JsonObject.SendMenu(container)).then(function (
          res
        ) {
          if (res.status == "ok") {
            alert("Correcto");
            window.location = "/";
          }
        });
      });
  };

  const JsonObject = (function () {
    return {
      SaveMenu: function (container) {
        return {
          fecha: container.find("#fechaMenu").val(),
        };
      },
      SaveMeal: function (container) {
        return {
          key: container.find("#platilloNombre").val(),
          description: container.find("#platilloDescripcion").val(),
          idMenu: container.find("input[id='id']").val(),
        };
      },
      SendMenu: function (container) {
        let objectMeals = [];
        $("#tablaComidasPedido")
          .find("tbody tr")
          .each(function (e) {
            objectMeals.push({
              id: $(this).attr("data-id"),
              key: $(this).children().first().text(),
              description: $(this).children().first().next().text(),
            });
          });

        return {
          menu: {
            id: container.find("input[id='id']").val(),
            publisheddate: container.find("#fechaMenu").val(),
          },
          meals: objectMeals,
        };
      },
    };
  })();

  const InitialActionsModule = (container) => {
    let id = container.find("input[id='id']").val()
      ? container.find("input[id='id']").val()
      : undefined;
    if (id != undefined) {
      container.find("#contenidoPlatillos").show();
      container.find("button[id='btnGuardarMenu']").hide();
      $("#contenidoListadoPlatillos").show();
      $("button[id='btnSendMenu']").show();
    } else {
      container.find("#contenidoPlatillos").hide();
      container.find("button[id='btnGuardarMenu']").show();
      $("#contenidoListadoPlatillos").hide();
      $("button[id='btnSendMenu']").hide();
    }
  };

  return {
    inicializar: function () {
      initializeModule();
    },
  };
})();

const MenuController = (function () {
  return {
    saveMenu: function (data) {
      return $.post("/saveMenu", JSON.stringify(data)).fail(function (
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
    saveMeal: function (data) {
      return $.post("/saveMeal", JSON.stringify(data)).fail(function (
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
    sendMenu: function (data) {
      return $.post("/sendMenu", JSON.stringify(data)).fail(function (
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

Menu.inicializar();
