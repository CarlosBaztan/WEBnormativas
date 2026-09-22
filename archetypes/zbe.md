---
title: "ZBE {{ replace .Name "-" " " | title }}"
description: ""
date: {{ .Date }}

# --- Identificación territorial ---
municipio: ""
provincia: ""
ccaa: ""

# --- Estado de la ZBE ---
# activa | prevista | sin_zbe
estado_zbe: "prevista"
fecha_vigor: ""

# --- Restricciones (dejar vacío si no se ha verificado) ---
etiquetas_permitidas: []   # ej. ["0", "ECO", "C"]
horario_restriccion: ""
excepciones: []

# --- Trazabilidad (OBLIGATORIO antes de publicar) ---
fuente_nombre: ""
fuente_url: ""
fecha_verificacion: ""

# --- Control de publicación ---
# verificado | pendiente
# REGLA DURA: pendiente => draft: true. No publicar datos sin verificar.
estado_dato: "pendiente"
draft: true
---

<!--
INSTRUCCIONES PARA PUBLICAR ESTA FICHA

1. Rellena los datos leyendo la ordenanza municipal oficial.
2. Cita fuente_nombre (ej. "Ordenanza municipal art. 7, BOP Zaragoza") y fuente_url.
3. Pon fecha_verificacion con el día en que lo comprobaste (YYYY-MM-DD).
4. Solo entonces: estado_dato: "verificado" y draft: false.

Si solo sabes que existe la ZBE pero no las reglas (nivel C):
  - estado_zbe: "activa"
  - etiquetas_permitidas: []  (vacío)
  - estado_dato: "pendiente"
La ficha NO se publica. Nunca respondas "¿puedo entrar?" sin datos.
-->
