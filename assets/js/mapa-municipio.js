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
        // Las grandes primero: se dibujan debajo.
        zona.sort(function (a, b) { return (b.properties.km2 || 0) - (a.properties.km2 || 0); });

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

        /*
         * Un municipio puede tener varias zonas de tamanos muy distintos.
         * Madrid tiene el termino municipal entero (1.152 km2) y dos ZBEDEP
         * de 6,3 y 1,6. Pintadas igual, las pequenas no se ven.
         */
        var UMBRAL_KM2 = 50;
        var deCiudad = function (p) { return (p.km2 || 0) >= UMBRAL_KM2; };

        var capa = L.geoJSON(zona, {
          style: function (f) {
            return deCiudad(f.properties)
              ? { color: '#57606a', weight: 1.5, dashArray: '6 5',
                  fillColor: '#57606a', fillOpacity: 0.06 }
              : { color: '#1a7f37', weight: 2.5,
                  fillColor: '#1a7f37', fillOpacity: 0.3 };
          },
          onEachFeature: function (f, c) {
            if (f.properties.zona) c.bindTooltip(f.properties.zona, { sticky: true });
            if (!deCiudad(f.properties)) c.bringToFront();
          }
        }).addTo(mapa);

        /*
         * Se encuadra en las zonas pequenas cuando las hay: encuadrar en la
         * municipal dejaria las ZBEDEP como dos puntos invisibles, que es
         * justo el problema que este cambio viene a resolver.
         */
        var pequenas = zona.filter(function (f) { return !deCiudad(f.properties); });
        var referencia = pequenas.length
          ? L.geoJSON(pequenas).getBounds()
          : capa.getBounds();
        mapa.fitBounds(referencia, { padding: [16, 16] });

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
