"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import re
import pandas as pd

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    ruta = "files/input/clusters_report.txt"

    with open(ruta, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    registros = []
    actual = ""
    capturando = False

    for linea in lineas:
        linea_limpia = linea.strip()

        if re.match(r"^\d+\s+\d+\s+", linea_limpia):
            if actual:
                registros.append(actual.strip())
            actual = linea_limpia
            capturando = True

        else:
            if capturando:
                actual += " " + linea_limpia

        if linea_limpia.endswith("."):
            capturando = False

    if actual:
        registros.append(actual.strip())

    patron = re.compile(r"^(\d+)\s+(\d+)\s+([\d,]+ ?%)\s+(.+)$")

    filas = []
    for reg in registros:
        match = patron.match(reg)
        if match:
            filas.append(match.groups())

    df = pd.DataFrame(filas, columns=[
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave",
        "principales_palabras_clave"
    ])

    df.columns = [c.lower() for c in df.columns]

    df["principales_palabras_clave"] = (
        df["principales_palabras_clave"]
        .str.replace(r"\s+", " ", regex=True)
        .str.replace(r"\s*,\s*", ", ", regex=True)
        .str.rstrip(".")
    )

    df["cluster"] = df["cluster"].astype(int)
    df["cantidad_de_palabras_clave"] = df["cantidad_de_palabras_clave"].astype(int)
    df["porcentaje_de_palabras_clave"] = (
        df["porcentaje_de_palabras_clave"]
        .str.replace("%", "")
        .str.replace(",", ".")
        .astype(float)
    )

    return df

print(pregunta_01())
print(pregunta_01().principales_palabras_clave.to_list()[1])
