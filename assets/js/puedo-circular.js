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

  // Municipios publicables. Vienen del front matter de las fichas con
  // estado_dato: "verificado"; ver el comentario en layouts/index.html.
  var MUNICIPIOS = leerJSON('datos-municipios') || [];

  // Rutas de las imágenes de los distintivos, procesadas por Hugo (llevan
  // hash en el nombre). Si falta el bloque, el recuadro sale solo con texto:
  // la imagen ilustra, no informa.
  var IMAGENES = leerJSON('datos-distintivos-img') || {};

  /*
   * La imagen es decorativa: el nombre del distintivo va escrito justo al
   * lado, así que un alt que lo repita solo estorba al lector de pantalla.
   */
  function imagenDistintivo(clave) {
    var i = IMAGENES[clave];
    if (!i) return '';
    return '<img class="distintivo-img distintivo-img--resultado"' +
      ' src="' + esc(i.src) + '"' +
      ' srcset="' + esc(i.src) + ' 1x, ' + esc(i.src2x) + ' 2x"' +
      ' width="' + i.ancho + '" height="' + i.alto + '"' +
      ' alt="" aria-hidden="true" decoding="async">';
  }

  function municipioPorSlug(slug) {
    for (var i = 0; i < MUNICIPIOS.length; i++) {
      if (MUNICIPIOS[i].slug === slug) return MUNICIPIOS[i];
    }
    return null;
  }

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
        imagenDistintivo(res.distintivo) +
        '<div class="pc-distintivo__texto">' +
        '<p class="pc-distintivo__etiqueta">Distintivo que probablemente le corresponde</p>' +
        '<p class="pc-distintivo__valor">' + esc(d ? d.nombre : res.distintivo) + '</p>' +
        (d && d.color ? '<p class="pc-distintivo__color">Color: ' + esc(d.color) + '</p>' : '') +
        '</div></div>' + extra;
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

  /*
   * Un municipio puede tener varias zonas con reglas distintas (Madrid tiene
   * tres). Se responde POR ZONA: una respuesta única seria falsa.
   *
   * `distintivos_permitidos` de una zona puede ser:
   *   - un array: ["0", "ECO", "C con condiciones"]
   *   - la cadena "pendiente": esa zona no se ha verificado todavia
   */

  // "C con condiciones" -> { clave: "C", condicionado: true }
  function analizarEntrada(entrada) {
    var txt = String(entrada).trim();
    var m = /^(0|ECO|C|B)\b\s*(.*)$/i.exec(txt);
    if (!m) return { clave: null, texto: txt, condicionado: false };
    var clave = m[1].toUpperCase();
    return { clave: clave, texto: txt, condicionado: m[2].trim().length > 0 };
  }

  /*
   * Veredicto de una zona para un distintivo concreto.
   * Devuelve: "permitido" | "condicionado" | "no_figura" | "pendiente" | "sin_distintivo_usuario"
   */
  function veredictoZona(zona, distintivoUsuario) {
    var permitidos = zona.distintivos_permitidos;
    if ((typeof permitidos === 'string') || !permitidos || !permitidos.length) return 'pendiente';
    if (!distintivoUsuario) return 'sin_distintivo_usuario';
    var entradas = permitidos.map(analizarEntrada);
    for (var i = 0; i < entradas.length; i++) {
      if (entradas[i].clave === distintivoUsuario) {
        return entradas[i].condicionado ? 'condicionado' : 'permitido';
      }
    }
    return 'no_figura';
  }

  var TEXTO_VEREDICTO = {
    permitido:   { etiqueta: 'Sí',              clase: 'si',   icono: '✓' },
    condicionado:{ etiqueta: 'Solo con condiciones', clase: 'cond', icono: '!' },
    no_figura:   { etiqueta: 'No',              clase: 'no',   icono: '×' },
    pendiente:   { etiqueta: 'Sin verificar',   clase: 'pend', icono: '?' },
    sin_distintivo_usuario: { etiqueta: 'Indica tu vehículo', clase: 'pend', icono: '?' }
  };

  /*
   * Resumen arriba del todo: la respuesta a "¿puedo circular?", zona por zona.
   * Sigue siendo atribuida a la ordenanza, no una autorización nuestra.
   */
  function pintarVeredicto(m, distintivoUsuario) {
    var zonas = m.zonas || [];
    if (!zonas.length) return '';

    var veredictos = zonas.map(function (z) { return veredictoZona(z, distintivoUsuario); });
    var hay = function (v) { return veredictos.indexOf(v) !== -1; };

    var titular;
    var claseGlobal;
    var soloVerificadas = veredictos.filter(function (v) { return v !== 'pendiente'; });

    // Todas las zonas verificadas coinciden => respuesta única.
    // Solo si difieren tiene sentido decir "depende de la zona".
    var todasIgual = function (v) {
      return soloVerificadas.length > 0 && soloVerificadas.every(function (x) { return x === v; });
    };
    var plural = soloVerificadas.length > 1;

    if (!distintivoUsuario) {
      titular = 'Necesitamos saber tu distintivo para responder';
      claseGlobal = 'pend';
    } else if (!soloVerificadas.length) {
      titular = 'Todavía no podemos responder por ' + esc(m.municipio);
      claseGlobal = 'pend';
    } else if (todasIgual('permitido')) {
      titular = plural ? 'Sí, en las zonas que hemos verificado' : 'Sí, según la ordenanza';
      claseGlobal = 'si';
    } else if (todasIgual('no_figura')) {
      titular = plural ? 'No, en ninguna de las zonas verificadas' : 'No, según la ordenanza';
      claseGlobal = 'no';
    } else if (todasIgual('condicionado')) {
      titular = 'Solo si cumples ciertas condiciones';
      claseGlobal = 'cond';
    } else {
      titular = 'Depende de la zona';
      claseGlobal = hay('no_figura') ? 'no' : 'cond';
    }

    var partes = ['<div class="pc-veredicto pc-veredicto--' + claseGlobal + '">'];
    partes.push('<p class="pc-veredicto__pregunta">¿Puedes circular por ' + esc(m.municipio) + '?</p>');
    partes.push('<p class="pc-veredicto__titular">' + titular + '</p>');

    partes.push('<ul class="pc-veredicto__zonas">');
    for (var i = 0; i < zonas.length; i++) {
      var t = TEXTO_VEREDICTO[veredictos[i]];
      partes.push('<li class="pc-vz pc-vz--' + t.clase + '">' +
        '<span class="pc-vz__icono" aria-hidden="true">' + t.icono + '</span>' +
        '<span class="pc-vz__zona">' + esc(zonas[i].nombre || zonas[i].id) + '</span>' +
        '<span class="pc-vz__valor">' + t.etiqueta + '</span>' +
        '</li>');
    }
    partes.push('</ul>');

    if (hay('condicionado')) {
      partes.push('<p class="pc-veredicto__nota">«Solo con condiciones» significa que tu distintivo figura, ' +
        'pero la ordenanza exige algo más: ser residente, tener actividad en la zona o acreditar un destino concreto. ' +
        'Lo detallamos debajo.</p>');
    }

    // La sigla aparece en los nombres oficiales de las zonas y no se explica sola.
    var usaZbedep = zonas.some(function (z) {
      return /ZBEDEP/i.test(String(z.nombre || ''));
    });
    if (usaZbedep) {
      partes.push('<p class="pc-veredicto__sigla">ZBEDEP: Zona de Bajas Emisiones de Especial Protección.</p>');
    }

    partes.push('</div>');
    return partes.join('');
  }

  function pintarZona(zona, distintivoUsuario) {
    var partes = ['<div class="pc-zona">'];
    partes.push('<h4>' + esc(zona.nombre || zona.id || 'Zona') + '</h4>');

    var permitidos = zona.distintivos_permitidos;
    var pendiente = (typeof permitidos === 'string') || !permitidos || !permitidos.length;

    if (pendiente) {
      partes.push('<p class="pc-zona__pendiente"><strong>Pendiente de verificar.</strong> ' +
        'No hemos contrastado todavía qué distintivos permite esta zona, así que no respondemos por ella.</p>');
      if (zona.nota) partes.push('<p class="pc-nota">' + esc(zona.nota) + '</p>');
    } else {
      var entradas = permitidos.map(analizarEntrada);
      partes.push('<p>La ordenanza nombra estos distintivos: <strong>' +
        entradas.map(function (e) { return esc(e.texto); }).join(', ') + '</strong>.</p>');

      if (distintivoUsuario) {
        var coincide = null;
        for (var i = 0; i < entradas.length; i++) {
          if (entradas[i].clave === distintivoUsuario) { coincide = entradas[i]; break; }
        }
        // "un vehículo con distintivo Sin distintivo" suena a error; se redacta aparte.
        var sujeto = distintivoUsuario === 'sin'
          ? 'Un vehículo <strong>sin distintivo ambiental</strong>'
          : 'Un vehículo con distintivo <strong>' + esc(nombreDistintivo(distintivoUsuario)) + '</strong>';

        if (coincide && coincide.condicionado) {
          partes.push('<p class="pc-cruce pc-cruce--condicional">' + sujeto +
            ' figura, pero <strong>' + esc(coincide.texto.replace(/^(0|ECO|C|B)\s*/i, '')) +
            '</strong>. Comprueba si cumples esas condiciones en el texto oficial.</p>');
        } else if (coincide) {
          partes.push('<p class="pc-cruce pc-cruce--si">' + sujeto +
            ' figura entre los que la ordenanza nombra para esta zona.</p>');
        } else {
          partes.push('<p class="pc-cruce pc-cruce--no">' + sujeto +
            ' no figura entre los que la ordenanza nombra para esta zona.</p>');
        }
      }

      if (zona.prohibidos && zona.prohibidos.length) {
        partes.push('<p>Expresamente excluidos: <strong>' +
          zona.prohibidos.map(function (p) { return esc(p); }).join(', ') + '</strong>.</p>');
      }
      if (zona.horario) partes.push('<p>Horario: ' + esc(zona.horario) + '</p>');
      if (zona.nota) partes.push('<p class="pc-nota">' + esc(zona.nota) + '</p>');
    }

    if (zona.articulo) {
      partes.push('<p class="pc-articulo">Referencia: ' + esc(zona.articulo) + '</p>');
    }
    partes.push('</div>');
    return partes.join('');
  }

  function pintarMunicipio(slug, distintivoUsuario) {
    if (!slug) {
      return '<div class="pc-aviso"><p>No has elegido municipio, así que no podemos contrastarlo con ninguna ordenanza.</p></div>';
    }

    var m = municipioPorSlug(slug);
    if (!m) {
      return '<div class="pc-aviso pc-aviso--sindatos">' +
        '<p class="pc-aviso__titulo">Todavía no hemos verificado la ordenanza de este municipio</p>' +
        '<p>Preferimos no decir nada a decir algo sin comprobar. Consulta la ordenanza del ayuntamiento antes de circular.</p>' +
        '</div>';
    }

    // El veredicto va fuera del recuadro de la ordenanza: es la respuesta,
    // no el detalle. Y justo después, el acceso a la ficha completa.
    var salida = [pintarVeredicto(m, distintivoUsuario)];

    if (m.url) {
      salida.push('<a class="pc-cta" href="' + esc(m.url) + '">' +
        'Ficha completa de ' + esc(m.municipio) +
        '<span class="pc-cta__flecha" aria-hidden="true">→</span></a>');
    }

    var partes = ['<div class="pc-ordenanza">'];
    partes.push('<h3>Lo que dice la ordenanza de ' + esc(m.municipio) + '</h3>');

    var zonas = m.zonas || [];
    if (zonas.length > 1) {
      partes.push('<p class="pc-nota">' + esc(m.municipio) + ' tiene ' + zonas.length +
        ' zonas con reglas distintas. Estas son las de cada una.</p>');
    }

    if (!zonas.length) {
      partes.push('<p class="pc-zona__pendiente">No consta ninguna zona verificada para este municipio.</p>');
    } else {
      for (var i = 0; i < zonas.length; i++) {
        partes.push(pintarZona(zonas[i], distintivoUsuario));
      }
    }

    partes.push('<p class="pc-nota">Esto resume una norma; no es una autorización. Contrasta siempre con el ' +
      'texto oficial y con la señalización de la zona. La decisión y la responsabilidad son tuyas.</p>');

    if (m.fuente_nombre) {
      var fuente = m.fuente_url
        ? '<a href="' + esc(m.fuente_url) + '" rel="noopener" target="_blank">' + esc(m.fuente_nombre) + '</a>'
        : esc(m.fuente_nombre);
      var boletin = m.fuente_boletin ? ' · ' + esc(m.fuente_boletin) : '';
      var fecha = m.fecha_verificacion ? ' · Verificado el ' + esc(formatearFecha(m.fecha_verificacion)) : '';
      partes.push('<p class="pc-fuente">Fuente: ' + fuente + boletin + fecha + '</p>');
    }

    partes.push('</div>');
    salida.push(partes.join(''));
    return salida.join('');
  }

  /*
   * Acepta "2026-09-23" y también "2026-09-23T00:00:00Z": Hugo convierte el
   * front matter a fecha y jsonify la serializa en ISO completo.
   */
  function formatearFecha(iso) {
    var m = /^(\d{4})-(\d{2})-(\d{2})(?:[T ].*)?$/.exec(String(iso).trim());
    if (!m) return iso;
    var mes = parseInt(m[2], 10), dia = parseInt(m[3], 10);
    if (mes < 1 || mes > 12 || dia < 1 || dia > 31) return iso;
    return m[3] + '/' + m[2] + '/' + m[1];
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

    // Orden: qué distintivo tienes, la respuesta, el acceso a la ficha, y
    // después el detalle. El aviso sobre la DGT va detrás: es importante,
    // pero no debe interponerse entre la pregunta y su respuesta.
    salida.innerHTML =
      pintarDistintivo(res) +
      pintarMunicipio(slug, res.distintivo) +
      bloqueConsultaOficial();

    var anclaAnuncio = document.getElementById('anuncio-bajo-resultado');
    if (anclaAnuncio) anclaAnuncio.hidden = false;

    // Llevar al usuario al resultado: en móvil suele quedar fuera de pantalla.
    // scroll-margin-top en el CSS evita que la cabecera fija lo tape.
    try {
      salida.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (e) {
      salida.scrollIntoView(); // navegadores sin soporte de opciones
    }
    // Y mover el foco, para que quien navega con teclado o lector de
    // pantalla aterrice también en el resultado, no solo la vista.
    salida.setAttribute('tabindex', '-1');
    salida.focus({ preventScroll: true });
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
