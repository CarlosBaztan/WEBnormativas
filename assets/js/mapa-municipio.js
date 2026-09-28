/*
 * Perimetro de una sola ZBE, dentro de su ficha.
 *
 * Reutiliza el mismo GeoJSON que /mapa/ y se queda con la zona cuyo slug
 * coincide con el de la ficha. Es mas trafico del necesario (176 KB para
 * pintar una zona), pero a cambio el navegador lo cachea y quien navegue
 * entre fichas y el mapa general no vuelve a descargarlo.
 */

(function () {
  'use strict';

  var DATOS = '/datos/zbe-simplificado.geojson';

  function arranca() {
    var contenedor = document.getElementById('mapa-municipio');
    if (!contenedor) return;

    var slug = contenedor.getAttribute('data-slug');
    if (!slug || typeof L === 'undefined') {
      contenedor.remove();
      return;
    }

    fetch(DATOS)
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (datos) {
        var zona = (datos.features || []).filter(function (f) {
          return f.properties && f.properties.slug === slug;
        });

        // Sin geometria para este municipio no se deja un hueco vacio: se
        // quita el bloque entero, atribucion incluida.
        if (!zona.length) {
          var att = contenedor.nextElementSibling;
          if (att && att.classList.contains('mapa-atribucion')) att.remove();
          contenedor.remove();
          return;
        }

        var mapa = L.map('mapa-municipio', {
          // Sin controles: aqui el mapa ilustra, no se explora. Para eso esta
          // el mapa general.
          zoomControl: false,
          dragging: false,
          scrollWheelZoom: false,
          doubleClickZoom: false,
          boxZoom: false,
          keyboard: false,
          touchZoom: false
        });

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          maxZoom: 18,
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(mapa);

        var capa = L.geoJSON(zona, {
          style: { color: '#1a7f37', weight: 2, fillColor: '#1a7f37', fillOpacity: 0.22 }
        }).addTo(mapa);

        mapa.fitBounds(capa.getBounds(), { padding: [16, 16] });

        var aviso = contenedor.querySelector('.mapa-zbe__cargando');
        if (aviso) aviso.remove();
      })
      .catch(function () {
        contenedor.remove();
      });
  }

  if (document.readyState === 'complete') {
    setTimeout(arranca, 0);
  } else {
    window.addEventListener('load', function () { setTimeout(arranca, 0); });
  }
})();
