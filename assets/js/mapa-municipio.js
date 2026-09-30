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
   * Aqui se pintan solo las zonas con restricciones propias.
   *
   * Madrid declara ademas el termino municipal entero (1.152 km2) como zona
   * de bajas emisiones, pero dibujarlo tapaba la ciudad de lado a lado y daba
   * a entender que esta cerrada por completo. Lo que restringe de verdad son
   * las dos ZBEDEP, y eso es lo que se ve. El resto lo cuenta la ficha.
   */
  function esContexto(p) {
    return !!p.envolvente;
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

  /* Quita el mapa y todo lo que solo tiene sentido con el delante. */
  function quitarBloque(contenedor) {
    var acompanan = ['mapa-ayuda', 'mapa-atribucion'];
    var siguiente = contenedor.nextElementSibling;
    while (siguiente) {
      var pertenece = acompanan.some(function (c) {
        return siguiente.classList.contains(c);
      });
      if (!pertenece) break;
      var aBorrar = siguiente;
      siguiente = siguiente.nextElementSibling;
      aBorrar.remove();
    }
    contenedor.remove();
  }

  function arranca() {
    var contenedor = document.getElementById('mapa-municipio');
    if (!contenedor) return;

    var slug = contenedor.getAttribute('data-slug');
    if (!slug || typeof L === 'undefined') {
      quitarBloque(contenedor);
      return;
    }

    fetch(DATOS)
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (datos) {
        var zona = (datos.features || []).filter(function (f) {
          return f.properties && f.properties.slug === slug && !esContexto(f.properties);
        });
        // Las grandes primero: se dibujan debajo.
        zona.sort(function (a, b) { return (b.properties.km2 || 0) - (a.properties.km2 || 0); });

        // Sin geometria para este municipio no se deja un hueco vacio: se
        // quita el bloque entero, ayuda y atribucion incluidas.
        //
        // Se recorren TODOS los hermanos que pertenecen al mapa, no solo el
        // siguiente: al anadir el parrafo de ayuda entre el contenedor y la
        // atribucion, la comprobacion de nextElementSibling dejo de
        // encontrarla, y en las paginas sin mapa (/zbe/que-es/) quedaban a la
        // vista las instrucciones de un mapa que no existe.
        if (!zona.length) {
          quitarBloque(contenedor);
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

        /* El mismo magenta del mapa general: no aparece en el mapa base de
           OpenStreetMap, asi que el perimetro no se confunde con un parque
           ni con una carretera. */
        var capa = L.geoJSON(zona, {
          style: function () {
            return { color: '#d6006e', weight: 3, opacity: 0.95,
                     fillColor: '#d6006e', fillOpacity: 0.3 };
          },
          onEachFeature: function (f, c) {
            if (f.properties.zona) c.bindTooltip(f.properties.zona, { sticky: true });
          }
        }).addTo(mapa);

        var referencia = capa.getBounds();

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
        quitarBloque(contenedor);
      });
  }

  if (document.readyState === 'complete') {
    setTimeout(arranca, 0);
  } else {
    window.addEventListener('load', function () { setTimeout(arranca, 0); });
  }
})();
