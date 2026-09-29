/*
 * Perimetro de una sola ZBE, dentro de su ficha.
 *
 * Reutiliza el mismo GeoJSON que /mapa/ y se queda con la zona cuyo slug
 * coincide con el de la ficha. Es mas trafico del necesario (183 KB para
 * pintar una zona), pero a cambio el navegador lo cachea y quien navegue
 * entre fichas y el mapa general no vuelve a descargarlo.
 *
 * Este mapa nacio inmovil, con la idea de que aqui solo ilustra. Era un error:
 * la ZBEDEP de Distrito Centro en 320 pixeles de alto no deja leer ni una
 * calle, y quien quiere saber si su calle esta dentro necesita acercarse.
 * Ahora se puede mover y ampliar, con los mismos gestos que el mapa grande.
 */

(function () {
  'use strict';

  var DATOS = '/datos/zbe-simplificado.geojson';

  /*
   * Un municipio puede tener varias zonas de tamanos muy distintos. Madrid
   * tiene el termino municipal entero (1.152 km2) y dos ZBEDEP de 6,3 y 1,6.
   * Pintadas igual, las pequenas no se ven.
   */
  var UMBRAL_KM2 = 50;

  function deCiudad(p) {
    return (p.km2 || 0) >= UMBRAL_KM2;
  }

  /*
   * Boton para volver al encuadre de partida.
   *
   * Desde que el mapa se puede mover, es facil acabar perdido en mitad de la
   * provincia sin saber como volver.
   */
  function botonVolver(mapa, encuadra) {
    var Volver = L.Control.extend({
      options: { position: 'topleft' },
      onAdd: function () {
        var caja = L.DomUtil.create('div', 'leaflet-bar mapa-volver');
        var boton = L.DomUtil.create('a', '', caja);
        boton.href = '#';
        boton.setAttribute('role', 'button');
        boton.innerHTML = '<svg viewBox="0 0 16 16" width="15" height="15" ' +
          'aria-hidden="true" focusable="false"><path fill="currentColor" ' +
          'd="M8 1.5 14.5 8 13.4 9.1 12.5 8.2V14H9.5v-3.5h-3V14h-3V8.2l-.9.9L1.5 8 8 1.5z"/></svg>';
        boton.title = 'Volver al encuadre de la zona';
        boton.setAttribute('aria-label', boton.title);
        L.DomEvent.on(boton, 'click', function (e) {
          L.DomEvent.stop(e);
          encuadra();
        });
        L.DomEvent.disableClickPropagation(caja);
        return caja;
      }
    });
    mapa.addControl(new Volver());
  }

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
          zoomSnap: 0.25,
          zoomDelta: 0.5,
          // Lo gobierna MapaGestos: rueda con Ctrl, dos dedos en tactil.
          scrollWheelZoom: false
        });

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          maxZoom: 18,
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(mapa);

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
         * justo el problema que este encuadre viene a resolver.
         */
        var pequenas = zona.filter(function (f) { return !deCiudad(f.properties); });
        var referencia = pequenas.length
          ? L.geoJSON(pequenas).getBounds()
          : capa.getBounds();

        function encuadra() {
          mapa.fitBounds(referencia, { padding: [16, 16] });
        }
        encuadra();

        if (window.MapaGestos) {
          MapaGestos.cooperativo(mapa, contenedor);
          MapaGestos.botonAmpliar(mapa, contenedor);
        }
        botonVolver(mapa, encuadra);

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
