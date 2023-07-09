document.addEventListener("DOMContentLoaded", function() {
  
  function actualizarContenido() {
    var claves = Object.keys(datosConsultaMonedas_js);
    var index = 0;
    
  
    return function() {
      var clave = claves[index];
      var valor = datosConsultaMonedas_js[clave];
  
      var label = document.getElementById("bandera");
      label.textContent = clave;
  
      var valorLabel = document.getElementById("valorMoneda");
      valorLabel.textContent = valor;
  
      index++;
      if (index >= claves.length) {
        index = 0;
      }
    };
  }
  
  
  // Crear una instancia de la función para realizar el seguimiento del índice
  var actualizar = actualizarContenido();

  // Llamar a la función actualizar inmediatamente
  actualizar();
  
  // Llamar a la función actualizar cada 5 segundos en un bucle infinito
  setInterval(actualizar, 5000);
  }
  );