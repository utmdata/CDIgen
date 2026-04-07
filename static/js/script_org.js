// =========================
// Variables globales
// =========================
let todasLasOrganizaciones = [];

// =========================
// URL SPARQL EDMO
// =========================
const ORGANIZATIONS_SPARQL_URL = 'https://edmo.seadatanet.org/sparql/sparql?query=SELECT%20%3Forg%20%3Fname%20%3FaltName%20%3Fnotation%20%3Fstreet%20%3Fpostal%20%3Flocality%20%3Fcountry%20%3Femail%20%3Ftel%20%3Fweb%20WHERE%20%7B%20%3Forg%20a%20%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Forg%23Organization%3E%20%3B%20%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Forg%23name%3E%20%3Fname%20.%20OPTIONAL%20%7B%20%3Forg%20%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23altName%3E%20%3FaltName%20%7D%20OPTIONAL%20%7B%20%3Forg%20%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23notation%3E%20%3Fnotation%20%7D%20OPTIONAL%20%7B%20%3Forg%20%3Chttp%3A%2F%2Fwww.w3.org%2F2006%2Fvcard%2Fns%23street-address%3E%20%3Fstreet%20%7D%20OPTIONAL%20%7B%20%3Forg%20%3Chttp%3A%2F%2Fwww.w3.org%2F2006%2Fvcard%2Fns%23postal-code%3E%20%3Fpostal%20%7D%20OPTIONAL%20%7B%20%3Forg%20%3Chttp%3A%2F%2Fwww.w3.org%2F2006%2Fvcard%2Fns%23locality%3E%20%3Flocality%20%7D%20OPTIONAL%20%7B%20%3Forg%20%3Chttp%3A%2F%2Fwww.w3.org%2F2006%2Fvcard%2Fns%23country-name%3E%20%3Fcountry%20%7D%20OPTIONAL%20%7B%20%3Forg%20%3Chttp%3A%2F%2Fwww.w3.org%2F2006%2Fvcard%2Fns%23email%3E%20%3Femail%20%7D%20OPTIONAL%20%7B%20%3Forg%20%3Chttp%3A%2F%2Fwww.w3.org%2F2006%2Fvcard%2Fns%23tel%3E%20%3Ftel%20%7D%20OPTIONAL%20%7B%20%3Forg%20%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23seeAlso%3E%20%3Fweb%20%7D%20%7D%20ORDER%20BY%20LCASE(%3Fname)&accept=application%2Fsparql-results%2Bjson';

// =========================
// Cargar organizaciones desde EDMO
// =========================
function cargarOrganizaciones() {
  console.log("cargarOrganizaciones() called");
  document.getElementById("overlay").style.display = "block";

  fetch(ORGANIZATIONS_SPARQL_URL)
    .then(response => response.text())
    .then(text => {
      let data;
      try {
        data = JSON.parse(text);
      } catch (e) {
        console.error("Respuesta SPARQL no es JSON válido:", text);
        throw e;
      }
      todasLasOrganizaciones = data?.results?.bindings || [];
      llenarListaDesplegable(todasLasOrganizaciones);
    })
    .catch(error => console.error("Fetch error:", error))
    .finally(() => document.getElementById("overlay").style.display = "none");
}


// =========================
// Llenar select con organizaciones
// =========================
function llenarListaDesplegable(organizaciones) {
  const select = document.getElementById('organizaciones');
  if (!select) return;

  select.innerHTML = '<option value="">Select organization*</option>';

  organizaciones.forEach(o => {
    const orgURI = o.org?.value;
    const name = o.name?.value;
    if (!orgURI || !name) return;

    const alt = o.altName?.value || '';
    const label = alt ? `${name} (${alt})` : name;

    const opt = document.createElement('option');
    opt.value = orgURI;
    opt.textContent = label;

    // Guardar metadata completa
    opt.dataset.org = JSON.stringify({
      uri: orgURI,
      name: name,
      altName: alt,
      notation: o.notation?.value || '',
      street: o.street?.value || '',
      postal: o.postal?.value || '',
      locality: o.locality?.value || '',
      country: o.country?.value || '',
      email: o.email?.value || '',
      tel: o.tel?.value || '',
      web: o.web?.value || ''
    });

    select.appendChild(opt);
  });

  console.log(`Se cargaron ${select.options.length - 1} organizaciones`);
}

// =========================
// Cargar resultados para organización seleccionada
// =========================
function cargarResultadosDesdeEnlace(organizacionURI) {
  const jsonDataURL = 'https://edmo.seadatanet.org/sparql/sparql?query=SELECT%20%3Forg%20%3Fname%20WHERE%20%7B%20%3Forg%20a%20%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Forg%23Organization%3E%20%3B%20%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2Fmodified%3E%20%3FmodifiedDate%20%3B%20%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Forg%23name%3E%20%3Fname%20.%20FILTER%28%3Forg%20%3D%20%3C' + encodeURIComponent(organizacionURI) + '%3E%29%20%7D&accept=*%2F*';
  fetch(jsonDataURL)
    .then(response => response.json())
    .then(data => mostrarResultados(data))
    .catch(error => console.error('Error al cargar los resultados desde EDMO:', error));
}

function mostrarResultados(resultados) {
  const resultadosDiv = document.getElementById('resultados');
  if (!resultadosDiv) return;
  resultadosDiv.innerHTML = '';

  (resultados.results?.bindings || []).forEach(resultado => {
    const orgURI = resultado.org?.value || '';
    const p = document.createElement('p');
    p.textContent = orgURI;
    resultadosDiv.appendChild(p);
  });
}

// =========================
// Manejar selección de organización
// =========================
function cargarResultadosSeleccionados() {
  const lista = document.getElementById('organizaciones');
  const orgURI = lista?.value;
  if (orgURI) cargarResultadosDesdeEnlace(orgURI);
}

// =========================
// Cargar CSR y filtrar vessels
// =========================
function loadDoc() {
  console.log("loadDoc() called");
  document.getElementById("overlay").style.display = "block";
  const csrUrl = 'static/csrCodeList.xml?ts=' + Date.now();

  fetch(csrUrl)
    .then(response => {
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
      return response.text();
    })
    .then(xmlString => {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(xmlString, "application/xml");
      if (xmlDoc?.documentElement?.nodeName === "parsererror") {
        console.error("XML parsing error:", xmlDoc);
      } else {
        filtrevessel(xmlDoc);
      }
      document.getElementById("overlay").style.display = "none";
    })
    .catch(error => {
      console.error("Fetch error (csr):", error);
      document.getElementById("overlay").style.display = "none";
    });
}

function filtrevessel(xml) {
  const select = document.getElementById("cdSelect");
  if (!select) return;
  select.innerHTML = '';

  // Siempre inicializa codeDefinitions como lista vacía
  const codeDefinitions = xml.querySelectorAll("CodeDefinition") || [];
  if (!codeDefinitions.length) {
    console.error("No CodeDefinitions found in XML");
    return;
  }

  const selectedVessel = document.getElementById("vessel_input")?.value || 'select';

  codeDefinitions.forEach(cd => {
    const platformCode = cd.querySelector("platformcode")?.textContent;
    const cruisename = cd.querySelector("cruisename")?.textContent;
    if (!platformCode || !cruisename) return;

    if (
      (selectedVessel === "select" && (platformCode === "29AH" || platformCode === "29HE")) ||
      (selectedVessel === "sdg" && platformCode === "29AH") ||
      (selectedVessel === "hes" && platformCode === "29HE")
    ) {
      const option = document.createElement("option");
      option.value = cruisename;
      option.text = cruisename;
      select.add(option);
    }
  });
}


// =========================
// Ejecutar al cargar la página
// =========================
window.onload = function () {
  cargarOrganizaciones();
  //loadDoc();
};
