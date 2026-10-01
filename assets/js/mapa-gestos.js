/*
 * Gestos y pantalla completa, compartidos por los dos mapas del sitio.
 *
 * El problema que resuelve: un mapa de 70vh de alto dentro de un articulo
 * atrapa el scroll. Leaflet lo evita desactivando la rueda, pero entonces solo
 * se puede ampliar con los botones + y -, que es justo lo que se nos ha
 * reprochado. La salida es el gesto cooperativo, que es lo que hace Google
 * Maps cuando va incrustado:
 *
 *   - Rueda a secas: la pagina sigue bajando, y un aviso dice como ampliar.
 *   - Ctrl (o Cmd) + rueda: amplia el mapa. El pellizco en el panel tactil
 *     del portatil llega al navegador exactamente asi, de modo que tambien
 *     funciona sin tocar ninguna tecla.
 *   - Un dedo en pantalla tactil: desplaza la pagina.
 *   - Dos dedos: mueven y amplian el mapa.
 *   - Doble clic y mayusculas + recuadro: los trae Leaflet de serie.
 *
 * Todo esto es progresivo: si este fichero no carga, los mapas siguen
 * funcionando con sus botones.
 */

window.MapaGestos = (function () {
  'use strict';

  var ES_MAC = /Mac|iPhone|iPad|iPod/.test(
    (navigator.userAgentData && navigator.userAgentData.platform) ||
    navigator.platform || '');
  var TECLA = ES_MAC ? 'Cmd' : 'Ctrl';

  var SVG_AMPLIAR = '<svg viewBox="0 0 16 16" width="15" height="15" aria-hidden="true" focusable="false">' +
    '<path fill="currentColor" d="M2 2h5v1.6H3.6V7H2V2zm7 0h5v5h-1.6V3.6H9V2zM2 9h1.6v3.4H7V14H2V9zm10.4 0H14v5H9v-1.6h3.4V9z"/></svg>';
  var SVG_CERRAR = '<svg viewBox="0 0 16 16" width="15" height="15" aria-hidden="true" focusable="false">' +
    '<path fill="currentColor" d="M5.4 2H7v5H2V5.4h3.4V2zM9 2h1.6v3.4H14V7H9V2zM2 9h5v5H5.4v-3.4H2V9zm7 0h5v1.6h-3.4V14H9V9z"/></svg>';

  /* Rotulo flotante que explica el gesto. Es decorativo: lo que dice ya esta
     escrito en la pagina, encima del mapa, para quien use lector de pantalla. */
  function avisador(contenedor) {
    var aviso = document.createElement('div');
    aviso.className = 'mapa-gesto';
    aviso.setAttribute('aria-hidden', 'true');
    contenedor.appendChild(aviso);

    var temporizador = null;
    var ultimo = '';
    return function (texto) {
      if (texto !== ultimo) {
        aviso.textContent = texto;
        ultimo = texto;
      }
      aviso.classList.add('mapa-gesto--visible');
      clearTimeout(temporizador);
      temporizador = setTimeout(function () {
        aviso.classList.remove('mapa-gesto--visible');
        ultimo = '';
      }, 1800);
    };
  }

  /* Escalon minimo de zoom. Tiene que coincidir con el zoomSnap del mapa: si
     se pide menos que eso, Leaflet redondea al mismo nivel y no pasa nada. */
  var PASO = 0.25;

  function cooperativo(mapa, contenedor) {
    var avisa = avisador(contenedor);
    var acumulado = 0;

    /* De la rueda nos encargamos nosotros. Si la dejamos en manos de Leaflet
       no hay forma de dejar pasar el scroll cuando no hay modificador. */
    if (mapa.scrollWheelZoom) mapa.scrollWheelZoom.disable();

    contenedor.addEventListener('wheel', function (e) {
      if (!(e.ctrlKey || e.metaKey)) {
        avisa(TECLA + ' + rueda para ampliar el mapa');
        return;
      }
      /* Sin esto el navegador ampliaria la pagina entera, que es su gesto
         para ctrl + rueda. */
      e.preventDefault();
      /* deltaMode 1 cuenta lineas y 0 pixeles: el mismo giro da numeros de
         ordenes de magnitud distintos segun el navegador.

         Se acumula en vez de aplicarse suelto porque el pellizco del panel
         tactil manda decenas de eventos diminutos: uno a uno no llegarian al
         escalon minimo de zoom y el mapa no se moveria. */
      acumulado += -e.deltaY * (e.deltaMode === 1 ? 0.08 : 0.0035);
      if (Math.abs(acumulado) < PASO) return;
      var salto = Math.max(-1.5, Math.min(1.5, acumulado));
      acumulado = 0;
      mapa.setZoomAround(mapa.mouseEventToContainerPoint(e),
                         mapa.getZoom() + salto, { animate: false });
    }, { passive: false });

    if (!mapa.dragging) return;

    /* En pantalla tactil el mapa no debe atrapar el dedo. Arranca sin
       arrastre y solo lo activa cuando hay dos dedos encima.

       La escucha va en fase de captura porque Leaflet tiene la suya en este
       mismo contenedor: si fuera detras, el arrastre ya habria empezado. */
    var tactil = window.matchMedia && window.matchMedia('(pointer: coarse)').matches;
    if (tactil) mapa.dragging.disable();

    contenedor.addEventListener('touchstart', function (e) {
      if (e.touches.length > 1) mapa.dragging.enable();
      else mapa.dragging.disable();
    }, { passive: true, capture: true });

    contenedor.addEventListener('touchmove', function (e) {
      if (e.touches.length === 1) avisa('Usa dos dedos para mover el mapa');
    }, { passive: true });

    /* Con raton el arrastre es el gesto natural y no estorba a nadie. */
    contenedor.addEventListener('mousedown', function () {
      mapa.dragging.enable();
    }, { passive: true, capture: true });
  }

  /*
   * Boton de pantalla completa.
   *
   * No se usa la API de pantalla completa del navegador porque Safari en iPhone
   * no la admite fuera de los videos. Una clase que fija el contenedor a la
   * ventana funciona en todas partes y ademas deja la cabecera del sitio
   * accesible con la tecla de escape.
   */
  function botonAmpliar(mapa, contenedor) {
    if (typeof L === 'undefined' || !L.Control) return;

    var Ampliar = L.Control.extend({
      options: { position: 'topleft' },

      onAdd: function () {
        var caja = L.DomUtil.create('div', 'leaflet-bar mapa-ampliar');
        var boton = L.DomUtil.create('a', '', caja);
        boton.href = '#';
        boton.setAttribute('role', 'button');
        pinta(false);

        L.DomEvent.on(boton, 'click', function (e) {
          L.DomEvent.stop(e);
          alterna();
        });
        /* Sin esto, un clic en el boton tambien llega al mapa y lo amplia. */
        L.DomEvent.disableClickPropagation(caja);

        function pinta(ampliado) {
          boton.innerHTML = ampliado ? SVG_CERRAR : SVG_AMPLIAR;
          var texto = ampliado
            ? 'Salir de la pantalla completa'
            : 'Ver el mapa a pantalla completa';
          boton.title = texto;
          boton.setAttribute('aria-label', texto);
          boton.setAttribute('aria-pressed', ampliado ? 'true' : 'false');
        }

        function alterna() {
          var ampliado = contenedor.classList.toggle('mapa--ampliado');
          document.body.classList.toggle('mapa-ampliado-activo', ampliado);
          pinta(ampliado);
          /* Leaflet guarda el tamano del contenedor: si cambia por CSS hay que
             decirselo o pinta los tiles donde ya no estan. */
          mapa.invalidateSize();
          if (!ampliado) boton.focus();
        }

        document.addEventListener('keydown', function (e) {
          if (e.key === 'Escape' && contenedor.classList.contains('mapa--ampliado')) {
            alterna();
          }
        });

        return caja;
      }
    });

    mapa.addControl(new Ampliar());
  }

  /*
   * Los botones de zoom de Leaflet, en espanol.
   *
   * Vienen con title="Zoom in" y "Zoom out" y no hay forma de cambiarlos
   * cuando el control lo crea el propio mapa (zoomControl: true). En un sitio
   * con <html lang="es">, un lector de pantalla los lee con fonetica
   * espanola y sale un ruido en vez de una palabra.
   *
   * aria-label ademas del title porque el title solo no es un nombre
   * accesible fiable: algunos lectores lo ignoran si hay contenido dentro del
   * enlace, y aqui lo hay (el signo + y el signo -).
   */
  function traducirZoom(contenedor) {
    var nombres = {
      'leaflet-control-zoom-in': 'Acercar el mapa',
      'leaflet-control-zoom-out': 'Alejar el mapa'
    };
    Object.keys(nombres).forEach(function (clase) {
      var boton = contenedor.querySelector('.' + clase);
      if (!boton) return;
      boton.title = nombres[clase];
      boton.setAttribute('aria-label', nombres[clase]);
    });
  }

  return { cooperativo: cooperativo, botonAmpliar: botonAmpliar,
           traducirZoom: traducirZoom, tecla: TECLA, paso: PASO };
})();
