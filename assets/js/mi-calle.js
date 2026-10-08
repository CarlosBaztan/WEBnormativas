/*
 * Herramienta "¿Está mi calle dentro de una ZBE?"
 *
 * Cruza una dirección con los perímetros que publica la DGT en su Punto de
 * Acceso Nacional, extraídos por pipeline/zbe_geometria.py.
 *
 * REGLAS DE NEGOCIO:
 *
 *  1. Nunca una respuesta binaria por cuenta propia. Se dice que la dirección
 *     cae dentro del perímetro QUE PUBLICA LA DGT, y se remite a la ordenanza,
 *     que es quien fija el perímetro oficial.
 *  2. La dirección se muestra tal y como la ha entendido el geocodificador,
 *     antes de responder. "Calle Mayor" existe en cientos de municipios: si se
 *     resuelve en el que no es, la respuesta sería falsa y creíble a la vez.
 *  3. La dirección NO se guarda ni se envía a ningún servidor nuestro. Va a
 *     Nominatim y se descarta.
 *  4. Si algo falla, se dice y se ofrece el mapa. No se adivina.
 */

(function () {
  'use strict';

  var DATOS = '/datos/zbe-simplificado.geojson';
  // Nominatim de OpenStreetMap. Su política de uso pide una petición por
  // segundo como máximo y que la aplicación se identifique.
  var GEOCODER = 'https://nominatim.openstreetmap.org/search';
  var ESPERA_MS = 1100;

  var form = document.getElementById('form-mi-calle');
  var salida = document.getElementById('resultado-mi-calle');
  if (!form || !salida) return;

  var zonas = null;
  var ultimaPeticion = 0;

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function aviso(clase, titulo, cuerpo) {
    return '<div class="pc-aviso ' + clase + '">' +
      (titulo ? '<p class="pc-aviso__titulo">' + titulo + '</p>' : '') +
      '<p>' + cuerpo + '</p></div>';
  }

  /*
   * Punto en polígono por proyección de rayos. A mano: son 45 polígonos, no
   * merece una dependencia.
   *
   * Cuenta cuántas veces un rayo horizontal hacia el este cruza los lados del
   * anillo. Impar significa dentro.
   */
  function dentroDeAnillo(punto, anillo) {
    var x = punto[0], y = punto[1];
    var dentro = false;
    for (var i = 0, j = anillo.length - 1; i < anillo.length; j = i++) {
      var xi = anillo[i][0], yi = anillo[i][1];
      var xj = anillo[j][0], yj = anillo[j][1];
      var cruza = ((yi > y) !== (yj > y)) &&
                  (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
      if (cruza) dentro = !dentro;
    }
    return dentro;
  }

  function dentroDeFeature(punto, feature) {
    var g = feature.geometry;
    var poligonos = g.type === 'Polygon' ? [g.coordinates] : g.coordinates;
    for (var p = 0; p < poligonos.length; p++) {
      // El primer anillo es el contorno; los siguientes serían agujeros.
      if (dentroDeAnillo(punto, poligonos[p][0])) return true;
    }
    return false;
  }

  function cargarZonas() {
    if (zonas) return Promise.resolve(zonas);
    return fetch(DATOS)
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) { zonas = d.features || []; return zonas; });
  }

  function geocodificar(texto) {
    var url = GEOCODER + '?format=jsonv2&limit=1&countrycodes=es&addressdetails=1&q=' +
      encodeURIComponent(texto);
    return fetch(url, { headers: { 'Accept': 'application/json' } })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
  }

  function pintarDentro(sitio, encontradas) {
    var partes = ['<div class="pc-veredicto pc-veredicto--no">'];
    partes.push('<p class="pc-veredicto__pregunta">La dirección que hemos entendido</p>');
    partes.push('<p class="pc-veredicto__titular">' + esc(sitio.display_name) + '</p>');
    partes.push('<p class="pc-veredicto__nota"><strong>Comprueba que es la tuya antes de seguir.</strong> ' +
      'Muchos nombres de calle se repiten en varios municipios.</p>');
    partes.push('</div>');

    partes.push('<div class="pc-ordenanza">');
    partes.push('<h3>Cae dentro de ' + (encontradas.length > 1 ? 'estas zonas' : 'esta zona') + '</h3>');
    partes.push('<ul class="mi-calle-zonas">');
    encontradas.forEach(function (f) {
      var p = f.properties;
      partes.push('<li><strong>' + esc(p.municipio) + '</strong>' +
        (p.url_ficha
          ? ' · <a href="' + esc(p.url_ficha) + '">qué dice su ordenanza</a>'
          : ' · <span class="dato-vacio">reglas sin verificar</span>') +
        '</li>');
    });
    partes.push('</ul>');
    partes.push('<p class="pc-nota"><strong>Esto no significa que no puedas entrar.</strong> ' +
      'Significa que esa dirección está dentro del perímetro que publica la DGT. ' +
      'Qué vehículos pueden circular lo decide la ordenanza del municipio, y el perímetro ' +
      'oficial también: contrástalo en la ficha y en la señalización de la calle.</p>');
    partes.push('</div>');

    if (encontradas.length === 1 && encontradas[0].properties.url_ficha) {
      partes.push('<a class="pc-cta" href="' + esc(encontradas[0].properties.url_ficha) + '">' +
        '¿Puede entrar mi coche en ' + esc(encontradas[0].properties.municipio) + '?' +
        '<span class="pc-cta__flecha" aria-hidden="true">→</span></a>');
    }
    return partes.join('');
  }

  function pintarFuera(sitio) {
    var partes = ['<div class="pc-veredicto pc-veredicto--si">'];
    partes.push('<p class="pc-veredicto__pregunta">La dirección que hemos entendido</p>');
    partes.push('<p class="pc-veredicto__titular">' + esc(sitio.display_name) + '</p>');
    partes.push('<p class="pc-veredicto__nota"><strong>Comprueba que es la tuya.</strong> ' +
      'Muchos nombres de calle se repiten en varios municipios.</p>');
    partes.push('</div>');
    partes.push('<div class="pc-ordenanza">');
    partes.push('<h3>No cae dentro de ninguna zona que publique la DGT</h3>');
    partes.push('<p>Hemos comprobado esa dirección contra los 45 perímetros de zonas de bajas ' +
      'emisiones que la DGT publica en su Punto de Acceso Nacional, y no está dentro de ninguno.</p>');
    partes.push('<p class="pc-nota">Ojo con lo que esto NO quiere decir. La DGT no publica el ' +
      'perímetro de todos los municipios con ZBE, y un ayuntamiento puede haber ampliado su zona ' +
      'sin que el dato haya llegado ahí. Si tu municipio tiene ZBE, mira su ficha y la señalización.</p>');
    partes.push('</div>');
    return partes.join('');
  }

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();

    var campo = document.getElementById('mi-calle-direccion');
    var texto = (campo.value || '').trim();

    /* El error lleva AL CAMPO, no al mensaje. Ver el porque largo en
       assets/js/puedo-circular.js: el `return` seco se saltaba el foco que si
       tiene la rama de exito, y el campo podia quedar fuera de pantalla. */
    campo.removeAttribute('aria-invalid');
    campo.removeAttribute('aria-describedby');

    if (texto.length < 5) {
      salida.innerHTML = aviso('pc-aviso--incierto', '',
        '<span id="mc-error-direccion">Escribe una dirección algo más completa: ' +
        'calle, número y municipio.</span>');
      campo.setAttribute('aria-invalid', 'true');
      campo.setAttribute('aria-describedby', 'mc-error-direccion');
      campo.focus();
      return;
    }

    var ahora = Date.now();
    if (ahora - ultimaPeticion < ESPERA_MS) {
      /* Aqui NO se marca `aria-invalid`: lo que escribio esta bien, lo que
         pasa es que ha pulsado demasiado rapido. Pero el foco si vuelve al
         campo, que es desde donde va a reintentar. */
      salida.innerHTML = aviso('pc-aviso--incierto', '',
        'Espera un segundo entre consultas, por favor. El servicio de búsqueda de ' +
        'direcciones es gratuito y conviene no saturarlo.');
      campo.focus();
      return;
    }
    ultimaPeticion = ahora;

    salida.innerHTML = '<p class="pc-ok">Buscando la dirección…</p>';

    Promise.all([cargarZonas(), geocodificar(texto)])
      .then(function (res) {
        var lista = res[0];
        var sitios = res[1];

        if (!sitios || !sitios.length) {
          salida.innerHTML = aviso('pc-aviso--sindatos', 'No hemos encontrado esa dirección',
            'Prueba a escribirla con el municipio, por ejemplo «Gran Vía 1, Madrid». ' +
            'También puedes buscarla a mano en <a href="/mapa/">el mapa de zonas</a>.');
          return;
        }

        var sitio = sitios[0];
        var punto = [parseFloat(sitio.lon), parseFloat(sitio.lat)];

        var encontradas = lista.filter(function (f) { return dentroDeFeature(punto, f); });
        salida.innerHTML = encontradas.length ? pintarDentro(sitio, encontradas) : pintarFuera(sitio);

        try { salida.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
        catch (e) { salida.scrollIntoView(); }
        salida.setAttribute('tabindex', '-1');
        salida.focus({ preventScroll: true });
      })
      .catch(function () {
        salida.innerHTML = aviso('pc-aviso--sindatos', 'No hemos podido hacer la comprobación',
          'El servicio de búsqueda de direcciones no ha respondido. ' +
          'Puedes mirarlo a mano en <a href="/mapa/">el mapa de zonas de bajas emisiones</a>.');
      });
  });
})();
