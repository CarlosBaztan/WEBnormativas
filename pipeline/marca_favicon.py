# -*- coding: utf-8 -*-
"""
Genera los iconos del sitio a partir del logotipo.

    python pipeline/marca_favicon.py

Escribe en static/: favicon.ico, favicon-16x16.png, favicon-32x32.png y
apple-touch-icon.png. Son las cuatro URL que declara
layouts/partials/head.html, y no deben cambiar de nombre: Google pide que la
direccion del icono sea estable y tarda de dias a semanas en releer una nueva.

POR QUE NO SE REDUCE EL PNG Y YA ESTA

El original (LogoCocheApto.png) es un render, no un vectorial. Tiene dos
problemas que solo se notan al bajar a 16 px:

  1. Ruido. El fondo no es blanco puro, va de 249 a 255, y los bordes llevan
     halo de compresion. Al reducir, ese ruido se promedia con el dibujo y
     ensucia la silueta: el coche sale gris en vez de negro.

  2. Margen de sobra. El logotipo ya trae un 10 % de aire dentro de su lienzo.
     El favicon anterior le sumaba otro 8 %, asi que de los 16 px utiles se
     gastaban casi 3 en nada.

Aqui se reconstruye por mascaras de color: cada pieza se vuelve a pintar con
su color plano exacto, se recorta al contenido y se deja un 3 % de margen.

EL FOTOGRAMA DE 16 PX VA APARTE

A 16 px el coche mide unos 7 px de alto. Los bujes de las ruedas y el hueco de
la ventanilla no caben, y dejarlos solo emborrona la silueta: se promedian con
el negro de alrededor y el coche se vuelve una mancha gris. Para ese tamanyo,
y solo para ese, se rellenan esos huecos y el coche se dibuja macizo.

De 32 px en adelante los detalles si caben y se conservan.

LO QUE ESTE SCRIPT NO ARREGLA

Que el logotipo lleva tres elementos (anillo, coche y tic) y a 16 px no hay
sitio para tres. Por mucho que se limpie, lo que se lee a ese tamanyo es un
circulo rojo con un tic verde; el coche se intuye. Eso no es un defecto del
proceso, es cuanta informacion cabe en 256 pixeles. Si algun dia se quiere un
icono tan nitido como el de las marcas que lo hacen bien, el camino es dibujar
una version reducida del logotipo (una sola pieza), no afinar mas esta.
"""

import os
import sys

from PIL import Image, ImageChops, ImageDraw

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGEN = os.path.join(RAIZ, "LogoCocheApto.png")
DESTINO = os.path.join(RAIZ, "static")

# Colores planos del logotipo, medidos sobre el original (media de cada pieza).
ROJO = (244, 60, 61)
VERDE = (101, 193, 69)
NEGRO = (33, 33, 29)

MARGEN = 0.03
FONDO = (255, 255, 255, 255)


def _umbral(banda, minimo):
    """Mascara blanca donde la banda llega al minimo."""
    return banda.point(lambda v: 255 if v >= minimo else 0, mode="L")


def _y(*mascaras):
    """Interseccion de mascaras de 0 y 255."""
    salida = mascaras[0]
    for m in mascaras[1:]:
        salida = ImageChops.multiply(salida, m)
    return salida


def mascaras(imagen):
    """Separa el logotipo en sus tres piezas por color."""
    r, g, b = imagen.split()
    mas_claro = ImageChops.lighter(ImageChops.lighter(r, g), b)

    rojo = _y(_umbral(r, 121),
              _umbral(ImageChops.subtract(r, g), 61),
              _umbral(ImageChops.subtract(r, b), 61))
    verde = _y(_umbral(g, 101),
               _umbral(ImageChops.subtract(g, r), 41),
               _umbral(ImageChops.subtract(g, b), 41))
    negro = mas_claro.point(lambda v: 255 if v < 110 else 0, mode="L")
    return rojo, verde, negro


def rellena_huecos(mascara):
    """Cierra los huecos rodeados por la pieza (bujes y ventanilla)."""
    ancho, alto = mascara.size
    # Un marco de 1 px garantiza que el exterior sea una sola region conexa,
    # aunque la pieza toque el borde del lienzo.
    marco = Image.new("L", (ancho + 2, alto + 2), 0)
    marco.paste(mascara, (1, 1))
    ImageDraw.floodfill(marco, (0, 0), 128)
    fuera = marco.crop((1, 1, ancho + 1, alto + 1))
    # Lo que no es exterior es la pieza o un hueco encerrado por ella.
    return fuera.point(lambda v: 0 if v == 128 else 255, mode="L")


def capa(mascara, color):
    lienzo = Image.new("RGBA", mascara.size, (*color, 255))
    lienzo.putalpha(mascara)
    return lienzo


def compon(rojo, verde, negro):
    """Orden de pintado: anillo, coche y el tic por encima."""
    lienzo = Image.new("RGBA", rojo.size, (0, 0, 0, 0))
    for mascara, color in ((rojo, ROJO), (negro, NEGRO), (verde, VERDE)):
        lienzo.alpha_composite(capa(mascara, color))
    return lienzo


def cuadra(fuente, lado, margen=MARGEN, fondo=FONDO):
    """
    Recorta al contenido, escala y centra en un cuadrado.

    Se compone al cuadruple y se reduce de una sola vez: un unico escalon de
    remuestreo deja el borde mas limpio que encadenar varios.
    """
    pieza = fuente.crop(fuente.getbbox())
    util = lado * (1 - 2 * margen)
    escala = util / max(pieza.width, pieza.height)
    grande = pieza.resize((max(1, round(pieza.width * escala * 4)),
                           max(1, round(pieza.height * escala * 4))),
                          Image.LANCZOS)
    lienzo = Image.new("RGBA", (lado * 4, lado * 4), fondo)
    lienzo.alpha_composite(grande, ((lado * 4 - grande.width) // 2,
                                    (lado * 4 - grande.height) // 2))
    return lienzo.resize((lado, lado), Image.LANCZOS)


def construir():
    original = Image.open(ORIGEN).convert("RGB")
    rojo, verde, negro = mascaras(original)

    detallado = compon(rojo, verde, negro)
    macizo = compon(rojo, verde, rellena_huecos(negro))

    f16 = cuadra(macizo, 16)
    f32 = cuadra(detallado, 32)
    f48 = cuadra(detallado, 48)
    f180 = cuadra(detallado, 180)
    return f16, f32, f48, f180


def main():
    f16, f32, f48, f180 = construir()

    f16.convert("RGB").save(os.path.join(DESTINO, "favicon-16x16.png"))
    f32.convert("RGB").save(os.path.join(DESTINO, "favicon-32x32.png"))
    f180.convert("RGB").save(os.path.join(DESTINO, "apple-touch-icon.png"))

    # Un .ico puede llevar una imagen distinta por tamanyo, y aqui hace falta:
    # el fotograma de 16 es el del coche macizo. Pillow lo permite con
    # append_images, siempre que no se le pase ademas `sizes`.
    f48.convert("RGB").save(os.path.join(DESTINO, "favicon.ico"),
                            append_images=[f32.convert("RGB"),
                                           f16.convert("RGB")])

    for nombre in ("favicon.ico", "favicon-16x16.png",
                   "favicon-32x32.png", "apple-touch-icon.png"):
        ruta = os.path.join(DESTINO, nombre)
        print("  %-22s %6d bytes" % (nombre, os.path.getsize(ruta)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
