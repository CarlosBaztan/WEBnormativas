/*
 * Herramienta "¿Puedo circular?"
 *
 * Deduce el distintivo ambiental de la DGT a partir del tipo de vehículo,
 * el combustible y la fecha de matriculación, y lo cruza con las reglas
 * de la ZBE del municipio elegido.
 *
 * REGLAS DE NEGOCIO (no tocar sin leer CLAUDE.md):
 *
 *  1. Las reglas salen de data/etiquetas_dgt.json, inyectado por Hugo.
 *     Nunca se codifican aquí a mano.
 *  2. El distintivo deducido es una APROXIMACIÓN. El real lo asigna la DGT
 *     en el Registro de Vehículos. Toda salida remite a la consulta oficial.
 *  3. Si no hay datos verificados de un municipio, se dice. Nunca se inventan.
 *  4. Nunca una respuesta binaria por cuenta propia: lo que se afirma se
 *     atribuye a la ordenanza, con fuente y fecha.
 *
 * Fuentes de las reglas (verificadas el 22/09/2026):
 *  - DGT: https://www.dgt.es/nuestros-servicios/tu-vehiculo/tus-vehiculos/distintivo-ambiental/
 *  - Ayuntamiento de Madrid: https://www.madrid.es/portales/munimadrid/es/Inicio/Movilidad-y-transportes/Distintivos-de-los-vehiculos-en-funcion-del-impacto-ambiental/
 */

(function () {
  'use strict';

  var CLAVE_PERFIL = 'perfil_vehiculo_v1';

  function leerJSON(id) {
    var el = document.getElementById(id);
    if (!el) return null;
    try {
      return JSON.parse(el.textContent);
    } catch (e) {
      return null;
    }
  }

  var ETIQUETAS = leerJSON('datos-etiquetas');
  var ZBE = leerJSON('datos-zbe');

  if (!ETIQUETAS) return; // Sin reglas no se deduce nada. El HTML sin JS ya explica qué hacer.

  var form = document.getElementById('form-circular');
  var salida = document.getElementById('resultado');
  var campoAutonomia = document.getElementById('campo-autonomia');
  var selTecnologia = document.getElementById('tecnologia');
  var selTipo = document.getElementById('tipo-vehiculo');
  var selMunicipio = document.getElementById('municipio');

  if (!form || !salida) return;

  // --- Almacenamiento local (puede fallar en incógnito) -------------------

  function guardarPerfil(perfil) {
    try {
      localStorage.setItem(CLAVE_PERFIL, JSON.stringify(perfil));
    } catch (e) { /* sin persistencia; la herramienta sigue funcionando */ }
  }

  function leerPerfil() {
    try {
      var raw = localStorage.getItem(CLAVE_PERFIL);
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      return null;
    }
  }

  function borrarPerfil() {
    try {
      localStorage.removeItem(CLAVE_PERFIL);
    } catch (e) { /* nada que hacer */ }
  }

  // --- Derivación del distintivo -----------------------------------------

  var TECNOLOGIAS_CERO = ['electrico_bateria', 'electrico_autonomia_extendida', 'pila_combustible'];
  var TECNOLOGIAS_ECO = ['hibrido_no_enchufable', 'gnc', 'gnl', 'glp'];

  function grupoDe(tipo) {
    return tipo === 'ocho_plazas_o_pesado' ? 'pesados_y_8_plazas' : 'ligeros';
  }

  /*
   * Compara una fecha de matriculación (año + mes) con los umbrales del JSON.
   * Devuelve { distintivo, incierto, motivo }.
   *
   * `mes` puede ser null: el usuario no lo sabe. En ese caso, si el año cae
   * justo en el umbral, no se elige por él — se devuelve `incierto` y la
   * interfaz muestra las dos posibilidades.
   */
  function porFecha(grupo, combustible, anio, mes) {
    var reglas = ETIQUETAS.reglas.por_combustible_y_fecha[grupo];
    if (!reglas || !reglas[combustible]) {
      return { distintivo: null, incierto: true, motivo: 'sin_reglas' };
    }
    var r = reglas[combustible];

    function anioDe(s) { return parseInt(s.slice(0, 4), 10); }
    function mesDe(s) { return parseInt(s.slice(5, 7), 10); }

    var umbralC = r.C && r.C.desde;
    var umbralB = r.B && r.B.desde;

    function cumple(umbral) {
      if (!umbral) return false;
      var ua = anioDe(umbral), um = mesDe(umbral);
      if (anio > ua) return true;
      if (anio < ua) return false;
      // Mismo año que el umbral: decide el mes.
      if (um === 1) return true;        // umbral en enero: todo el año cumple
      if (mes === null) return null;    // no lo sabemos y el mes importa
      return mes >= um;
    }

    var c = cumple(umbralC);
    if (c === null) {
      return { distintivo: null, incierto: true, motivo: 'mes_desconocido', entre: ['B', 'C'] };
    }
    if (c === true) return { distintivo: 'C', incierto: false };

    var b = cumple(umbralB);
    if (b === null) {
      return { distintivo: null, incierto: true, motivo: 'mes_desconocido', entre: ['sin', 'B'] };
    }
    if (b === true) return { distintivo: 'B', incierto: false };

    return { distintivo: 'sin', incierto: false };
  }

  function derivar(datos) {
    // Las motos tienen criterios propios que NO están en el JSON.
    // Ver _limitaciones_conocidas: no se deducen aquí.
    if (datos.tipo === 'moto') {
      return { distintivo: null, incierto: true, motivo: 'moto' };
    }

    if (TECNOLOGIAS_CERO.indexOf(datos.tecnologia) !== -1) {
      return { distintivo: '0', incierto: false };
    }

    if (datos.tecnologia === 'hibrido_enchufable') {
      if (datos.autonomia !== null && datos.autonomia >= 40) {
        return { distintivo: '0', incierto: false };
      }
      if (datos.autonomia === null) {
        return { distintivo: null, incierto: true, motivo: 'autonomia_desconocida', entre: ['0', 'ECO'] };
      }
      // PHEV de menos de 40 km: ECO si además cumple los criterios de C.
      return eco(datos);
    }

    if (TECNOLOGIAS_ECO.indexOf(datos.tecnologia) !== -1) {
      return eco(datos);
    }

    // Gasolina o diésel puros.
    return porFecha(grupoDe(datos.tipo), datos.tecnologia, datos.anio, datos.mes);
  }

  /*
   * Tecnologías ECO: el JSON exige "criterios_C" además de la tecnología.
   * El motor de combustión de estos vehículos es casi siempre de gasolina,
   * así que se usa su umbral. Se marca como aproximación porque el criterio
   * real depende de la homologación Euro concreta del vehículo.
   */
  function eco(datos) {
    var r = porFecha(grupoDe(datos.tipo), 'gasolina', datos.anio, datos.mes);
    if (r.distintivo === 'C') return { distintivo: 'ECO', incierto: false, aproximado: true };
    if (r.incierto) return { distintivo: null, incierto: true, motivo: 'mes_desconocido', entre: ['ECO', 'sin'] };
    return { distintivo: null, incierto: true, motivo: 'eco_antiguo' };
  }

  // --- Presentación -------------------------------------------------------

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  var enlaceDGT = (ETIQUETAS._meta && ETIQUETAS._meta.consulta_oficial) || '';

  function bloqueConsultaOficial() {
    if (!enlaceDGT) return '';
    return '<p class="pc-oficial">El distintivo real lo asigna la DGT en el Registro de Vehículos. ' +
      'Lo que ves aquí es una deducción a partir de los datos que has introducido: ' +
      '<a href="' + esc(enlaceDGT) + '" rel="noopener" target="_blank">compruébalo en la sede electrónica de la DGT</a>.</p>';
  }

  function nombreDistintivo(clave) {
    var d = ETIQUETAS.distintivos[clave];
    return d ? d.nombre : clave;
  }

  function pintarDistintivo(res) {
    if (res.distintivo) {
      var d = ETIQUETAS.distintivos[res.distintivo];
      var extra = res.aproximado
        ? '<p class="pc-nota">La asignación exacta depende de la homologación Euro concreta del vehículo.</p>'
        : '';
      return '<div class="pc-distintivo pc-distintivo--' + esc(res.distintivo) + '">' +
        '<p class="pc-distintivo__etiqueta">Distintivo que probablemente le corresponde</p>' +
        '<p class="pc-distintivo__valor">' + esc(d ? d.nombre : res.distintivo) + '</p>' +
        (d && d.color ? '<p class="pc-distintivo__color">Color: ' + esc(d.color) + '</p>' : '') +
        '</div>' + extra;
    }

    // Casos sin respuesta única: se explican, no se resuelven a ojo.
    var msg;
    if (res.motivo === 'moto') {
      msg = 'Las motocicletas y ciclomotores se rigen por criterios propios que esta herramienta no cubre. ' +
        'No vamos a deducir tu distintivo con reglas que no le aplican.';
    } else if (res.motivo === 'autonomia_desconocida') {
      msg = 'Falta la autonomía eléctrica. En un híbrido enchufable marca la diferencia entre el distintivo 0 ' +
        '(40 km o más) y el ECO (menos de 40 km).';
    } else if (res.motivo === 'mes_desconocido') {
      msg = 'Tu año de matriculación cae justo en el límite entre el distintivo ' +
        esc(nombreDistintivo(res.entre[0])) + ' y el ' + esc(nombreDistintivo(res.entre[1])) +
        '. Sin el mes no se puede determinar cuál es.';
    } else if (res.motivo === 'eco_antiguo') {
      msg = 'Esa tecnología obtiene el distintivo ECO solo si cumple además los criterios del distintivo C, ' +
        'y por su antigüedad no está claro que los cumpla.';
    } else {
      msg = 'No podemos determinar el distintivo con los datos introducidos.';
    }

    return '<div class="pc-aviso pc-aviso--incierto">' +
      '<p class="pc-aviso__titulo">No podemos afirmar qué distintivo te corresponde</p>' +
      '<p>' + msg + '</p></div>';
  }

  function pintarMunicipio(slug) {
    var municipios = (ZBE && ZBE.municipios) || {};
    var m = slug ? municipios[slug] : null;

    if (!slug) {
      return '<div class="pc-aviso"><p>No has elegido municipio, así que no podemos contrastarlo con ninguna ordenanza.</p></div>';
    }

    if (!m || m.confianza !== 'oficial') {
      return '<div class="pc-aviso pc-aviso--sindatos">' +
        '<p class="pc-aviso__titulo">Todavía no hemos verificado la ordenanza de este municipio</p>' +
        '<p>Sabemos que existe la zona, pero no hemos contrastado artículo por artículo qué distintivos ' +
        'pueden circular. Preferimos no decir nada a decir algo sin comprobar.</p>' +
        '<p>Consulta la ordenanza del ayuntamiento antes de circular.</p>' +
        '</div>';
    }

    var permitidas = m.etiquetas_permitidas || [];
    var partes = ['<div class="pc-ordenanza">'];
    partes.push('<h3>Lo que dice la ordenanza de ' + esc(m.municipio) + '</h3>');

    if (permitidas.length) {
      partes.push('<p>Distintivos que la ordenanza permite circular: <strong>' +
        permitidas.map(function (p) { return esc(nombreDistintivo(p)); }).join(', ') + '</strong>.</p>');
    }
    if (m.horario_restriccion) {
      partes.push('<p>Horario de restricción: ' + esc(m.horario_restriccion) + '</p>');
    }
    if (m.excepciones && m.excepciones.length) {
      partes.push('<p>Excepciones recogidas:</p><ul>' +
        m.excepciones.map(function (e) { return '<li>' + esc(e) + '</li>'; }).join('') + '</ul>');
    }
    if (m.fuente_nombre) {
      var fuente = m.fuente_url
        ? '<a href="' + esc(m.fuente_url) + '" rel="noopener" target="_blank">' + esc(m.fuente_nombre) + '</a>'
        : esc(m.fuente_nombre);
      var fecha = m.fecha_verificacion ? ' · Verificado el ' + esc(formatearFecha(m.fecha_verificacion)) : '';
      partes.push('<p class="pc-fuente">Fuente: ' + fuente + fecha + '</p>');
    }
    partes.push('</div>');
    return partes.join('');
  }

  function formatearFecha(iso) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(iso));
    if (!m) return iso;
    var mes = parseInt(m[2], 10), dia = parseInt(m[3], 10);
    if (mes < 1 || mes > 12 || dia < 1 || dia > 31) return iso;
    return m[3] + '/' + m[2] + '/' + m[1];
  }

  function cruzar(res, slug) {
    var municipios = (ZBE && ZBE.municipios) || {};
    var m = slug ? municipios[slug] : null;
    if (!m || m.confianza !== 'oficial' || !res.distintivo) return '';

    var permitidas = m.etiquetas_permitidas || [];
    if (!permitidas.length) return '';

    var entra = permitidas.indexOf(res.distintivo) !== -1;

    // Atribuido a la ordenanza, nunca afirmado por el sitio.
    return '<div class="pc-cruce ' + (entra ? 'pc-cruce--si' : 'pc-cruce--no') + '">' +
      '<p>Según esa ordenanza, un vehículo con distintivo <strong>' + esc(nombreDistintivo(res.distintivo)) +
      '</strong> ' + (entra ? 'figura entre los que pueden circular' : 'no figura entre los que pueden circular') +
      ' por la zona' + (m.horario_restriccion ? ' en el horario indicado' : '') + '.</p>' +
      '<p class="pc-nota">Esto resume una norma; no es una autorización. Contrasta siempre con el texto oficial ' +
      'y con la señalización de la zona. La decisión y la responsabilidad son tuyas.</p>' +
      '</div>';
  }

  // --- Eventos ------------------------------------------------------------

  function actualizarCampos() {
    var esPHEV = selTecnologia.value === 'hibrido_enchufable';
    if (campoAutonomia) campoAutonomia.hidden = !esPHEV;

    var esMoto = selTipo.value === 'moto';
    var fs = document.getElementById('grupo-combustion');
    if (fs) fs.hidden = esMoto;
  }

  if (selTecnologia) selTecnologia.addEventListener('change', actualizarCampos);
  if (selTipo) selTipo.addEventListener('change', actualizarCampos);

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();

    var anioRaw = document.getElementById('anio').value;
    var mesRaw = document.getElementById('mes').value;
    var autoRaw = document.getElementById('autonomia').value;

    var datos = {
      tipo: selTipo.value,
      tecnologia: selTecnologia.value,
      anio: anioRaw ? parseInt(anioRaw, 10) : null,
      mes: mesRaw ? parseInt(mesRaw, 10) : null,
      autonomia: autoRaw ? parseInt(autoRaw, 10) : null
    };

    if (datos.tipo !== 'moto' && (!datos.anio || datos.anio < 1900 || datos.anio > 2100)) {
      salida.innerHTML = '<div class="pc-aviso pc-aviso--incierto"><p>Introduce un año de matriculación válido.</p></div>';
      return;
    }

    guardarPerfil(datos);

    var res = derivar(datos);
    var slug = selMunicipio ? selMunicipio.value : '';

    salida.innerHTML =
      pintarDistintivo(res) +
      bloqueConsultaOficial() +
      pintarMunicipio(slug) +
      cruzar(res, slug);

    var anclaAnuncio = document.getElementById('anuncio-bajo-resultado');
    if (anclaAnuncio) anclaAnuncio.hidden = false;
  });

  var btnBorrar = document.getElementById('borrar-perfil');
  if (btnBorrar) {
    btnBorrar.addEventListener('click', function () {
      borrarPerfil();
      form.reset();
      actualizarCampos();
      salida.innerHTML = '<p class="pc-ok">Datos del vehículo borrados de este navegador.</p>';
    });
  }

  // Restaurar el perfil guardado, si lo hay.
  var guardado = leerPerfil();
  if (guardado) {
    if (guardado.tipo) selTipo.value = guardado.tipo;
    if (guardado.tecnologia) selTecnologia.value = guardado.tecnologia;
    if (guardado.anio) document.getElementById('anio').value = guardado.anio;
    if (guardado.mes) document.getElementById('mes').value = guardado.mes;
    if (guardado.autonomia) document.getElementById('autonomia').value = guardado.autonomia;
    var aviso = document.getElementById('aviso-guardado');
    if (aviso) aviso.hidden = false;
  }

  actualizarCampos();
})();
