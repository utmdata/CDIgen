// Variable para almacenar todas las organizaciones
let todasLasOrganizaciones = [];

// Función para cargar las organizaciones desde el enlace SPARQL
function cargarOrganizaciones() {
  // URL que devuelve todas las organizaciones en formato JSON
  const jsonDataURL = 'https://edmo.seadatanet.org/sparql/sparql?query=SELECT%20%3Forg%20(CONCAT(%3Fname%2C%20%22%20(%22%2C%20%3FaltName%2C%20%22)%22)%20AS%20%3ForgName)%20%3Fnotation%20%3Ftel%20%3FaltName%20%3Fstreet%20%3Fcodepostal%20%3Flocality%20%3Femail%20%3Fcountry%20%3Fweb%0D%0AWHERE%20%7B%0D%0A%20%20%20%20%3Forg%20a%20%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Forg%23Organization%3E%20%3B%0D%0A%20%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23altName%3E%20%3FaltName%20%3B%0D%0A%20%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Forg%23name%3E%20%3Fname%20%3B%0D%0A%20%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Fwww.w3.org%2F2006%2Fvcard%2Fns%23tel%3E%20%3Ftel%20%3B%0D%0A%20%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23notation%3E%20%3Fnotation%20%3B%0D%0A%20%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Fwww.w3.org%2F2006%2Fvcard%2Fns%23street-address%3E%20%3Fstreet%20%3B%0D%0A%20%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Fwww.w3.org%2F2006%2Fvcard%2Fns%23postal-code%3E%20%3Fcodepostal%20%3B%0D%0A%20%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Fwww.w3.org%2F2006%2Fvcard%2Fns%23locality%3E%20%3Flocality%20%3B%0D%0A%20%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Fwww.w3.org%2F2006%2Fvcard%2Fns%23email%3E%20%3Femail%20%3B%0D%0A%20%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Fwww.w3.org%2F2006%2Fvcard%2Fns%23country-name%3E%20%3Fcountry%20%3B%0D%0A%20%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23seeAlso%3E%20%3Fweb%20.%0D%0A%7D%0D%0AORDER%20BY%20%3Fname&accept=*%2F*';

  // Realizar la solicitud AJAX directamente al enlace
  fetch(jsonDataURL)
    .then(response => response.json())
    .then(data => {
      // Almacenar todas las organizaciones en la variable
      todasLasOrganizaciones = data.results.bindings;

      // Llenar la lista desplegable con las organizaciones
      llenarListaDesplegable(todasLasOrganizaciones);
    })
    .catch(error => {
      console.error('Error al cargar las organizaciones desde el enlace:', error);
      });
}

// Función para llenar la lista desplegable con las organizaciones
function llenarListaDesplegable(organizaciones) {
  const listaDesplegable = document.getElementById('organizaciones');

  // Limpiar cualquier contenido anterior en la lista desplegable
  listaDesplegable.innerHTML = '<option value="">Select organization*</option>';

  // Agregar las organizaciones a la lista desplegable
  organizaciones.forEach(organizacion => {
    const orgName = organizacion.orgName.value; // Se utiliza la propiedad orgName según la definición en el SPARQL
    const orgURI = organizacion.org.value;

    const optionElement = document.createElement('option');
    optionElement.value = orgURI;
    optionElement.textContent = orgName;

    listaDesplegable.appendChild(optionElement);
  });
}

// Función para realizar la búsqueda en la lista de organizaciones
function realizarBusqueda() {
  const campoBusqueda = document.getElementById('busqueda');
  const valorBusqueda = campoBusqueda.value.toLowerCase();

  // Filtrar las organizaciones según la búsqueda
  const resultadosFiltrados = todasLasOrganizaciones.filter(organizacion => {
    const nombre = organizacion.name.value.toLowerCase();
    return nombre.includes(valorBusqueda);
  });

  // Llenar la lista desplegable con los resultados filtrados
  llenarListaDesplegable(resultadosFiltrados);
}

// Función para cargar los resultados directamente desde el enlace
function cargarResultadosDesdeEnlace(organizacionURI) {
  // URL que devuelve los resultados en formato JSON
  const jsonDataURL = 'https://edmo.seadatanet.org/sparql/sparql?query=SELECT%20%3Forg%20%3Fname%20WHERE%20%7B%20%3Forg%20a%20%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Forg%23Organization%3E%20%3B%20%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2Fmodified%3E%20%3FmodifiedDate%20%3B%20%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Forg%23name%3E%20%3Fname%20.%20FILTER%28%3Forg%20%3D%20%3C' + encodeURIComponent(organizacionURI) + '%3E%29%20%7D&accept=*%2F*';

  // Realizar la solicitud AJAX directamente al enlace
  fetch(jsonDataURL)
    .then(response => response.json())
    .then(data => {
      // Manejar los resultados de la consulta y mostrarlos en la página
      mostrarResultados(data);
    })
    .catch(error => {
      console.error('Error al cargar los resultados desde el enlace:', error);
    });
}

// Función para mostrar los resultados en la página
function mostrarResultados(resultados) {
  const resultadosDiv = document.getElementById('resultados');

  // Limpiar cualquier contenido anterior
  resultadosDiv.innerHTML = '';

  // Crear elementos HTML para cada resultado
  resultados.results.bindings.forEach(resultado => {
    const orgName = resultado.name.value;
    const orgURI = resultado.org.value;



    const resultadoElemento = document.createElement('p');
    resultadoElemento.textContent = `${orgURI}`;//Organization ${orgName},

    resultadosDiv.appendChild(resultadoElemento);
  });
}

// Función para cargar los resultados cuando se selecciona una organización
function cargarResultadosSeleccionados() {
  const listaDesplegable = document.getElementById('organizaciones');
  const organizacionSeleccionada = listaDesplegable.value;

  // Cargar los resultados solo si se selecciona una organización
  if (organizacionSeleccionada) {
    cargarResultadosDesdeEnlace(organizacionSeleccionada);
  }
}

function loadDoc() {
  console.log("loadDoc() initated"); // Log a message to console indicating loadDoc() function is called
  document.getElementById("overlay").style.display = "block";
  
  //fetch response
  fetch("http://161.111.137.92:8001/static/csrCodeList.xml")
      .then(response => {
      if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.text();

      })
      .then(xmlString => {
      var parser = new DOMParser();
      var xmlDoc = parser.parseFromString(xmlString, "application/xml");

      // Verificar si xmlDoc es válido y tiene elementos CodeDefinition
      if (xmlDoc && xmlDoc.documentElement && xmlDoc.documentElement.nodeName === "parsererror") {
          console.error("XML parsing error:", xmlDoc);
      } else {
          filtrevessel(xmlDoc); //myFunction(xmlDoc); es carregaran tots els csr reference de 29AH i 29HE
      }
      // Hide the overlay after successful fetch
      document.getElementById("overlay").style.display = "none";
      console.log("loadDoc() successfull"); // Log a message to console indicating loadDoc() function is called

      })
      .catch(error => {
      console.error("Fetch error:", error);
      // Hide the overlay after successful fetch
      document.getElementById("overlay").style.display = "none";
      });
}
// funcio  per carregar 
function myFunction(xml) {
  var select = document.getElementById("cdSelect");
  var codeDefinitions = xml.querySelectorAll("CodeDefinition");

  // Verificar si hay CodeDefinitions
  if (codeDefinitions) {
    codeDefinitions.forEach(function (codeDefinition, index) {
      var platformCodeElement = codeDefinition.querySelector("platformcode");
      var cruisenameElement = codeDefinition.querySelector("cruisename");

      if (platformCodeElement && cruisenameElement) {
        var platformCode = platformCodeElement.textContent;
        var cruisename = cruisenameElement.textContent;

        // Aplicar filtro para mostrar solo los valores correspondientes a los platformcodes 29AH e 29HE
        if (platformCode === "29AH" || platformCode === "29HE") {
          var option = document.createElement("option");
          option.value = cruisename;
          option.text = cruisename;
          select.add(option);
        }
      }
    });


  } else {
    console.error("No CodeDefinitions found in the XML");
  }
}

function filtrevessel(xml) {
  var select = document.getElementById("cdSelect");
  var codeDefinitions = xml.querySelectorAll("CodeDefinition");


  // Obtener el valor seleccionado del "vessel"
  var selectedVessel = document.getElementById("vessel_input").value;

  // Verificar si hay CodeDefinitions
  if (codeDefinitions) {
    codeDefinitions.forEach(function (codeDefinition, index) {
      var platformCodeElement = codeDefinition.querySelector("platformcode");
      var cruisenameElement = codeDefinition.querySelector("cruisename");

      if (platformCodeElement && cruisenameElement) {
        var platformCode = platformCodeElement.textContent;
        var cruisename = cruisenameElement.textContent;

        // Aplicar filtro según el "vessel" seleccionado
        // Aplicar filtro para mostrar solo los valores correspondientes a los platformcodes 29AH e 29HE
        if (selectedVessel === "select" && platformCode === "29AH" && platformCode === "29HE") {
          var option = document.createElement("option");
          option.value = cruisename;
          option.text = cruisename;
          select.add(option);
        }
        else if (selectedVessel === "sdg" && platformCode === "29AH") {
          var option = document.createElement("option");
          option.value = cruisename;
          option.text = cruisename;
          select.add(option);
        } 
        else if (selectedVessel === "hes" && platformCode === "29HE") {
          var option = document.createElement("option");
          option.value = cruisename;
          option.text = cruisename;
          select.add(option);
        }
      }
    });
  } else {
    console.error("No CodeDefinitions found in the XML");
  }
}
// Llamar a la función para cargar las organizaciones cuando la página se carga
window.onload = function () {
  cargarOrganizaciones()  
};
  //loadDoc();

