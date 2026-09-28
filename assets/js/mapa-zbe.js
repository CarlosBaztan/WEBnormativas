/*
 * Mapa de las Zonas de Bajas Emisiones de Espana.
 *
 * Los perimetros salen de pipeline/zbe_geometria.py, que los extrae de los
 * ficheros DATEX2 del Punto de Acceso Nacional de la DGT. Licencia CC-BY: la
 * atribucion esta en la plantilla y es obligatoria.
 *
 * REGLAS DE NEGOCIO:
 *
 *  1. Nunca una respuesta binaria. El globo dice de donde sale el perimetro y
 *     remite a la ficha; no afirma que se pueda o no se pueda entrar.
 *  2. El enlace a la ficha sale de properties.url_ficha. No se construye aqui:
 *     una URL inventada seria un 404 desde el mapa.
 *  3. Si algo falla, la tabla de municipios de debajo sigue sirviendo el mismo
 *     dato. El mapa es un extra.
 */

(function () {
  'use strict';

  var CONTENEDOR = 'mapa-zbe';
  var DATOS = '/datos/zbe-simplificado.geojson';

  // Centro y zoom que encuadran la peninsula. Canarias queda fuera del encuadre
  // inicial a proposito: meterla obliga a alejar tanto que no se ve nada.
  var CENTRO = [40.0, -3.7];
  var ZOOM = 6;

  var COLORES = {
    verificado: '#1a7f37',
    parcial:    '#9a6700',
    pendiente:  '#57606a'
  };

  function color(estado) {
    return COLORES[estado] || COLORES.pendiente;
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function globo(p) {
    var partes = ['<strong>' + esc(p.municipio) + '</strong>'];
    if (p.provincia && p.provincia !== p.municipio) {
      partes.push('<span class="globo-provincia">' + esc(p.provincia) + '</span>');
    }

    if (p.url_ficha) {
      partes.push('<a class="globo-ficha" href="' + esc(p.url_ficha) + '">' +
        'Ver qué dice su ordenanza</a>');
    } else {
      partes.push('<span class="globo-nota">Todavía no hemos verificado sus reglas de acceso.</span>');
      if (p.fuente_url) {
        partes.push('<a class="globo-ficha" href="' + esc(p.fuente_url) +
          '" rel="noopener external" target="_blank">Fuente oficial</a>');
      }
    }

    partes.push('<span class="globo-aviso">El perímetro oficial lo fija la ordenanza municipal. ' +
      'Este trazado es el que publica la DGT.</span>');
    return partes.join('');
  }

  function fallo(mensaje) {
    var c = document.getElementById(CONTENEDOR);
    if (c) {
      c.innerHTML = '<p class="mapa-zbe__fallo">' + esc(mensaje) +
        ' Tienes el mismo dato en la tabla de municipios de más abajo.</p>';
    }
  }

  function arranca() {
    var contenedor = document.getElementById(CONTENEDOR);
    if (!contenedor) return;
    if (typeof L === 'undefined') {
      fallo('No se ha podido cargar el mapa.');
      return;
    }

    var mapa = L.map(CONTENEDOR, {
      center: CENTRO,
      zoom: ZOOM,
      // En movil, un mapa que captura el gesto de arrastre secuestra el scroll
      // de la pagina y es insoportable. Se activa al tocarlo.
      dragging: !L.Browser.mobile,
      scrollWheelZoom: false
    });

    mapa.on('focus', function () { mapa.scrollWheelZoom.enable(); });
    mapa.on('blur', function () { mapa.scrollWheelZoom.disable(); });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '&copy; colaboradores de <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(mapa);

    fetch(DATOS)
      .then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.json();
      })
      .then(function (datos) {
        var capa = L.geoJSON(datos, {
          style: function (f) {
            var c = color(f.properties.estado_dato);
            return { color: c, weight: 2, fillColor: c, fillOpacity: 0.25 };
          },
          onEachFeature: function (f, capaZona) {
            capaZona.bindPopup(globo(f.properties));
            // Accesible por teclado: sin esto el mapa solo existe para el raton.
            capaZona.bindTooltip(f.properties.municipio, { sticky: true });
          }
        }).addTo(mapa);

        var limites = capa.getBounds();
        if (limites.isValid()) mapa.fitBounds(limites, { padding: [20, 20] });

        var aviso = contenedor.querySelector('.mapa-zbe__cargando');
        if (aviso) aviso.remove();
      })
      .catch(function () {
        fallo('No se han podido cargar los perímetros.');
      });
  }

  // Despues del primer pintado: 175 KB de geometria no deben retrasar a que la
  // pagina sea legible.
  if (document.readyState === 'complete') {
    setTimeout(arranca, 0);
  } else {
    window.addEventListener('load', function () { setTimeout(arranca, 0); });
  }
})();
