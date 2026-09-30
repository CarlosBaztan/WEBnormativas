/*
 * Herramienta "¿Cuándo me toca la ITV?"
 *
 * REGLAS DE NEGOCIO (las mismas que el resto del sitio):
 *
 *  1. La tabla sale de data/itv_periodicidad.json, inyectado por Hugo desde
 *     el artículo 6.1 del RD 920/2017. Nunca se codifica aquí a mano.
 *  2. Lo que se afirma se atribuye a la norma, con su artículo y su fecha de
 *     verificación.
 *  3. La fecha exacta la fija la tarjeta ITV del vehículo, que se cuenta desde
 *     la última inspección. Esto calcula el vencimiento de la PRIMERA y la
 *     cadencia posterior, y lo dice en vez de fingir que sabe más.
 *  4. Si falta un dato, se dice; no se estima en silencio.
 */

(function () {
  'use strict';

  var CLAVE_PERFIL = 'perfil_vehiculo_v1';

  function leerJSON(id) {
    var el = document.getElementById(id);
    if (!el) return null;
    try { return JSON.parse(el.textContent); } catch (e) { return null; }
  }

  var DATOS = leerJSON('datos-itv');
  if (!DATOS) return;

  var form = document.getElementById('form-itv');
  var salida = document.getElementById('resultado-itv');
  if (!form || !salida) return;

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  /* localStorage revienta en navegación privada y con el almacenamiento
     bloqueado. Sin try/catch, la herramienta entera deja de responder al
     pulsar el botón. */
  function leerPerfil() {
    try { return JSON.parse(localStorage.getItem(CLAVE_PERFIL)) || null; }
    catch (e) { return null; }
  }

  function guardarPerfil(datos) {
    try {
      var previo = leerPerfil() || {};
      previo.tipo_itv = datos.categoria;
      previo.anio = datos.anio;
      previo.mes = datos.mes;
      localStorage.setItem(CLAVE_PERFIL, JSON.stringify(previo));
    } catch (e) { /* sin memoria la herramienta funciona igual, solo no recuerda */ }
  }

  var MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
               'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];

  function enLetra(fecha) {
    return fecha.getDate() + ' de ' + MESES[fecha.getMonth()] + ' de ' + fecha.getFullYear();
  }

  function sumaAnios(fecha, anios) {
    var d = new Date(fecha.getTime());
    d.setFullYear(d.getFullYear() + anios);
    return d;
  }

  function tramoDe(categoria, anios) {
    var tramos = DATOS.categorias[categoria].tramos;
    for (var i = 0; i < tramos.length; i++) {
      var t = tramos[i];
      if (anios >= t.desde_anios && (t.hasta_anios === null || anios < t.hasta_anios)) {
        return t;
      }
    }
    return null;
  }

  function pintar(categoria, matriculacion) {
    var cat = DATOS.categorias[categoria];
    var hoy = new Date();
    var anios = (hoy - matriculacion) / (365.2425 * 24 * 3600 * 1000);
    var tramo = tramoDe(categoria, anios);
    if (!tramo) {
      return '<div class="pc-aviso"><p>No hemos podido determinar la periodicidad con esos datos.</p></div>';
    }

    var per = DATOS.periodicidades[tramo.periodicidad];
    var exento = tramo.periodicidad === 'exento';

    var noExentos = cat.tramos.filter(function (t) { return t.periodicidad !== 'exento'; });
    var primerTramo = noExentos.length ? noExentos[0] : null;
    var primeraITV = primerTramo ? sumaAnios(matriculacion, primerTramo.desde_anios) : null;

    /*
     * Este bloque es la PREMISA, no la respuesta.
     *
     * Antes repetia aqui la periodicidad (per.nombre) y la volvia a decir el
     * veredicto tres lineas mas abajo, ademas con un cuerpo mayor: la copia
     * pesaba mas que el original. Con los recuadros de antes parecian dos
     * cosas distintas; en cuanto se quitaron, la duplicacion quedo a la
     * vista. Aqui va lo que se ha deducido del formulario, y la respuesta
     * se da una sola vez.
     */
    var partes = ['<div class="pc-distintivo pc-distintivo--itv"><div class="pc-distintivo__texto">'];
    partes.push('<p class="pc-distintivo__etiqueta">Tu vehículo</p>');
    partes.push('<p class="pc-distintivo__valor">' + esc(cat.nombre) + '</p>');
    partes.push('<p class="pc-distintivo__color">' + esc(cat.categoria_legal) +
      ', matriculado hace ' + Math.floor(anios) + ' años</p>');
    partes.push('</div></div>');

    if (exento && primeraITV) {
      partes.push('<div class="pc-veredicto pc-veredicto--si">');
      partes.push('<p class="pc-veredicto__pregunta">¿Cuándo te toca?</p>');
      partes.push('<p class="pc-veredicto__titular">Todavía no</p>');
      partes.push('<p class="pc-veredicto__nota">Tu primera inspección vence el <strong>' +
        esc(enLetra(primeraITV)) + '</strong>, cuando el vehículo cumpla ' +
        primerTramo.desde_anios + ' años.</p>');
      partes.push('</div>');
    } else {
      partes.push('<div class="pc-veredicto pc-veredicto--cond">');
      partes.push('<p class="pc-veredicto__pregunta">¿Cuándo te toca?</p>');
      partes.push('<p class="pc-veredicto__titular">' + esc(per.nombre) + '</p>');
      if (per.explicacion) {
        partes.push('<p class="pc-veredicto__detalle">' + esc(per.explicacion) + '</p>');
      }
      partes.push('<p class="pc-veredicto__nota"><strong>La fecha exacta está en la tarjeta ITV de tu vehículo.</strong> ' +
        'Se cuenta desde la última inspección que pasaste, no desde la matriculación, ' +
        'así que esta herramienta no puede saberla: lo que te dice es cada cuánto te toca.</p>');
      if (primeraITV) {
        partes.push('<p class="pc-veredicto__sigla">Tu primera inspección venció el ' +
          esc(enLetra(primeraITV)) + '.</p>');
      }
      partes.push('</div>');
    }

    partes.push('<div class="pc-ordenanza"><h3>Cómo cambia con la edad del vehículo</h3><ul class="itv-tramos">');
    cat.tramos.forEach(function (t) {
      var esActual = t === tramo;
      var rango;
      if (t.hasta_anios === null) {
        rango = 'A partir de los ' + t.desde_anios + ' años';
      } else if (t.desde_anios === 0) {
        rango = 'Hasta los ' + t.hasta_anios + ' años';
      } else {
        rango = 'De ' + t.desde_anios + ' a ' + t.hasta_anios + ' años';
      }
      partes.push('<li' + (esActual ? ' class="itv-tramo--actual"' : '') + '>' +
        '<span>' + esc(rango) + '</span><span>' +
        esc(DATOS.periodicidades[t.periodicidad].nombre) + '</span></li>');
    });
    partes.push('</ul>');
    partes.push('<p class="pc-fuente">Fuente: <a href="' + esc(DATOS._meta.fuente_url) +
      '" rel="noopener external" target="_blank">' + esc(DATOS._meta.fuente_nombre) +
      '<span class="visually-hidden"> (se abre en una ventana nueva)</span></a>' +
      ' · Verificado el 29 de septiembre de 2026</p>');
    partes.push('</div>');

    return partes.join('');
  }

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();

    var categoria = document.getElementById('itv-categoria').value;
    var anio = parseInt(document.getElementById('itv-anio').value, 10);
    var mes = parseInt(document.getElementById('itv-mes').value, 10);

    if (!categoria || !DATOS.categorias[categoria]) {
      salida.innerHTML = '<div class="pc-aviso pc-aviso--incierto"><p>Elige el tipo de vehículo.</p></div>';
      return;
    }
    if (!anio || anio < 1900 || anio > 2100) {
      salida.innerHTML = '<div class="pc-aviso pc-aviso--incierto"><p>Introduce un año de matriculación válido.</p></div>';
      return;
    }

    guardarPerfil({ categoria: categoria, anio: anio, mes: mes || null });

    /* Sin mes se cuenta desde enero: es el supuesto que hace al vehículo más
       viejo, así que nunca le dice a nadie que va más sobrado de lo que va. */
    var matriculacion = new Date(anio, (mes ? mes - 1 : 0), 1);
    var aviso = mes ? '' :
      '<p class="pc-nota">No has indicado el mes, así que hemos contado desde enero. ' +
      'Con el mes exacto la fecha se afina.</p>';

    salida.innerHTML = pintar(categoria, matriculacion) + aviso;

    try { salida.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    catch (e) { salida.scrollIntoView(); }
    salida.setAttribute('tabindex', '-1');
    salida.focus({ preventScroll: true });
  });

  /* Reutiliza el perfil que el usuario ya metió en "¿Puedo circular?": quien
     ya describió su coche no lo vuelve a describir. */
  var guardado = leerPerfil();
  if (guardado) {
    var sel = document.getElementById('itv-categoria');
    if (guardado.tipo_itv && DATOS.categorias[guardado.tipo_itv]) {
      sel.value = guardado.tipo_itv;
    } else if (guardado.tipo && DATOS.categorias[guardado.tipo]) {
      sel.value = guardado.tipo;
    }
    if (guardado.anio) document.getElementById('itv-anio').value = guardado.anio;
    if (guardado.mes) document.getElementById('itv-mes').value = guardado.mes;
    var nota = document.getElementById('itv-recuperado');
    if (nota && (guardado.anio || guardado.tipo_itv || guardado.tipo)) nota.hidden = false;
  }
})();
