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

  /*
   * Umbral en km2 por encima del cual una zona se considera "de ciudad".
   *
   * Madrid tiene una zona de 1.152 km2 (el termino municipal entero) y dos
   * ZBEDEP de 6,3 y 1,6. Pintadas igual, las pequenas desaparecen debajo de
   * la grande y el mapa da a entender que toda la ciudad esta restringida,
   * que no es lo que pasa.
   *
   * Las grandes van con trazo discontinuo y relleno casi transparente; las
   * pequenas, solidas y por encima.
   */
  var UMBRAL_KM2 = 50;

  /*
   * Por encima de este nivel de zoom se retiran las chinchetas: ya se esta
   * mirando una ciudad concreta y el perimetro se ve solo.
   */
  var ZOOM_SIN_CHINCHETAS = 11;

  function esDeCiudad(p) {
    return (p.km2 || 0) >= UMBRAL_KM2;
  }

  function estilo(f) {
    var p = f.properties;
    var c = color(p.estado_dato);
    if (esDeCiudad(p)) {
      return { color: c, weight: 1.5, dashArray: '6 5', fillColor: c, fillOpacity: 0.06 };
    }
    return { color: c, weight: 2.5, fillColor: c, fillOpacity: 0.38 };
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function globo(p) {
    var partes = ['<strong>' + esc(p.municipio) + '</strong>'];
    if (p.zona) {
      partes.push('<span class="globo-zona">' + esc(p.zona) + '</span>');
    }
    if (p.provincia && p.provincia !== p.municipio) {
      partes.push('<span class="globo-provincia">' + esc(p.provincia) + '</span>');
    }
    if (p.zona && esDeCiudad(p)) {
      partes.push('<span class="globo-nota">Esta zona abarca todo el municipio. ' +
        'Dentro hay otras con reglas mas estrictas: son las que se ven marcadas encima.</span>');
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

  /*
   * Agrupa las zonas por municipio.
   *
   * El mapa tiene 57 zonas repartidas en 45 municipios, y quien busca Madrid
   * quiere Madrid entero, no una de sus tres zonas. El selector y las
   * chinchetas trabajan sobre municipios; los poligonos, sobre zonas.
   */
  function porMunicipio(capas) {
    var indice = {};
    capas.forEach(function (c) {
      var p = c.feature.properties;
      if (!indice[p.slug]) {
        indice[p.slug] = { slug: p.slug, municipio: p.municipio,
                           estado: p.estado_dato, capas: [] };
      }
      indice[p.slug].capas.push(c);
    });
    return Object.keys(indice).map(function (k) { return indice[k]; })
      .sort(function (a, b) { return a.municipio.localeCompare(b.municipio, 'es'); });
  }

  /*
   * Encuadre de un municipio.
   *
   * Cuando tiene zonas pequenas se encuadra en ellas: encuadrar en la
   * municipal dejaria las ZBEDEP como dos puntos invisibles, que es justo el
   * problema que se quiere evitar.
   */
  function zonasQueImportan(grupo) {
    var pequenas = grupo.capas.filter(function (c) {
      return !esDeCiudad(c.feature.properties);
    });
    return pequenas.length ? pequenas : grupo.capas;
  }

  function limitesDe(grupo) {
    var limites = null;
    zonasQueImportan(grupo).forEach(function (c) {
      limites = limites ? limites.extend(c.getBounds()) : L.latLngBounds(c.getBounds());
    });
    return limites;
  }

  /*
   * Zona cuyo globo se abre al llegar.
   *
   * Es la mayor de las que han decidido el encuadre, no la mas pequena del
   * municipio: en Madrid, el encuadre lo manda Distrito Centro y abrir el
   * globo de Plaza Eliptica dejaba el cartel hablando de una zona distinta de
   * la que se estaba viendo.
   */
  function zonaPrincipal(grupo) {
    return zonasQueImportan(grupo).reduce(function (a, b) {
      return (a.feature.properties.km2 || 0) >= (b.feature.properties.km2 || 0) ? a : b;
    });
  }

  function llevaA(mapa, grupo) {
    var limites = limitesDe(grupo);
    if (!limites || !limites.isValid()) return;
    mapa.flyToBounds(limites, { padding: [40, 40], maxZoom: 15, duration: 0.8 });
    var zona = zonaPrincipal(grupo);
    mapa.once('moveend', function () { zona.openPopup(); });
  }

  /*
   * Chinchetas por municipio.
   *
   * Alejado, las 45 ciudades son manchas de pocos pixeles sobre el mapa de
   * Espana: solo se distingue la de Madrid, que abarca el termino municipal
   * entero. Sin estos puntos, la pagina no dice donde hay zonas de bajas
   * emisiones, que es lo primero que se le pide.
   */
  function chinchetas(mapa, grupos) {
    var capa = L.layerGroup();

    grupos.forEach(function (g) {
      var limites = limitesDe(g);
      if (!limites || !limites.isValid()) return;
      var punto = L.circleMarker(limites.getCenter(), {
        radius: 6,
        weight: 2,
        color: '#fff',
        fillColor: color(g.estado),
        fillOpacity: 1
      });
      punto.bindTooltip(g.municipio, { direction: 'top' });
      punto.on('click', function () { llevaA(mapa, g); });
      capa.addLayer(punto);
    });

    capa.addTo(mapa);

    // Acercado ya estorban: el perimetro se ve solo y el punto tapa calles.
    function revisa() {
      var toca = mapa.getZoom() < ZOOM_SIN_CHINCHETAS;
      if (toca && !mapa.hasLayer(capa)) capa.addTo(mapa);
      if (!toca && mapa.hasLayer(capa)) mapa.removeLayer(capa);
    }
    mapa.on('zoomend', revisa);
    revisa();
  }

  /*
   * Selector de municipio. Sin el, la unica forma de encontrar una ciudad es
   * ampliar a ojo sobre el mapa de Espana.
   */
  function selector(mapa, grupos, limitesTodo) {
    var caja = document.querySelector('.mapa-ir');
    var lista = document.getElementById('mapa-ir-select');
    if (!caja || !lista) return;

    grupos.forEach(function (g) {
      var op = document.createElement('option');
      op.value = g.slug;
      op.textContent = g.municipio +
        (g.capas.length > 1 ? ' (' + g.capas.length + ' zonas)' : '');
      lista.appendChild(op);
    });

    lista.addEventListener('change', function () {
      var g = grupos.filter(function (x) { return x.slug === lista.value; })[0];
      if (g) llevaA(mapa, g);
    });

    var todo = caja.querySelector('.mapa-ir__todo');
    if (todo) {
      todo.addEventListener('click', function () {
        lista.value = '';
        mapa.closePopup();
        if (limitesTodo && limitesTodo.isValid()) {
          mapa.flyToBounds(limitesTodo, { padding: [20, 20], duration: 0.8 });
        }
      });
    }

    caja.hidden = false;
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
      /* Escalones de cuarto de nivel: el zoom por rueda y por pellizco avanza
         de poco en poco, y con el escalon de serie, que es un nivel entero,
         la mayoria de los gestos no llegaban a mover nada. */
      zoomSnap: 0.25,
      zoomDelta: 0.5,
      /* Los gestos los gobierna MapaGestos: rueda con Ctrl y dos dedos en
         pantalla tactil. Aqui solo se apaga lo que Leaflet haria por su
         cuenta, que es secuestrar el scroll de la pagina. */
      scrollWheelZoom: false
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '&copy; colaboradores de <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(mapa);

    if (window.MapaGestos) {
      MapaGestos.cooperativo(mapa, contenedor);
      MapaGestos.botonAmpliar(mapa, contenedor);
    }

    fetch(DATOS)
      .then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.json();
      })
      .then(function (datos) {
        var capas = [];
        var capa = L.geoJSON(datos, {
          style: estilo,
          onEachFeature: function (f, capaZona) {
            capaZona.bindPopup(globo(f.properties));
            // Accesible por teclado: sin esto el mapa solo existe para el raton.
            var rotulo = f.properties.zona
              ? f.properties.municipio + ': ' + f.properties.zona
              : f.properties.municipio;
            capaZona.bindTooltip(rotulo, { sticky: true });
            // Las pequenas al frente: si no, quedan tapadas por la municipal
            // y no se pueden ni pulsar.
            if (!esDeCiudad(f.properties)) capaZona.bringToFront();
            capas.push(capaZona);
          }
        }).addTo(mapa);

        var limites = capa.getBounds();
        if (limites.isValid()) mapa.fitBounds(limites, { padding: [20, 20] });

        var grupos = porMunicipio(capas);
        chinchetas(mapa, grupos);
        selector(mapa, grupos, limites);

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
