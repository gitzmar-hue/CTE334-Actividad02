"""
CTE-334 - Desarrollo de Aplicaciones SIG
Actividad 02 - Distancia y direccion con interfaz grafica
Autor: Gitzy Yissel Andrade Andrade
Numero de cuenta: 20161030363
Fecha: 15 de octube 2026
"""

import math
import tkinter as tk
from tkinter import messagebox, ttk

# Radio medio de la Tierra segun el valor indicado en la guia de la actividad
RADIO_TIERRA_KM = 6371.0088

LINEA = "-" * 40


# ---------------------------------------------------------------------------
# Logica geografica (misma responsabilidad y resultados que la Actividad 01).
# Estas funciones no dependen de widgets ni muestran ventanas emergentes.
# ---------------------------------------------------------------------------

def validar_coordenadas(latitud, longitud):
    """Comprueba que la latitud y la longitud esten dentro de los rangos
    geograficos permitidos (-90 <= latitud <= 90, -180 <= longitud <= 180).

    Retorna True si ambos valores son validos, False en caso contrario.
    """
    return -90 <= latitud <= 90 and -180 <= longitud <= 180


def calcular_distancia(lat1, lon1, lat2, lon2):
    """Calcula la distancia entre dos puntos geograficos aplicando la
    formula de Haversine. Recibe las coordenadas en grados decimales y
    retorna la distancia resultante en kilometros.
    """
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2) ** 2
         + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)

    distancia = 2 * RADIO_TIERRA_KM * math.asin(math.sqrt(a))
    return distancia


def determinar_direccion(lat1, lon1, lat2, lon2):
    """Compara las latitudes y longitudes del Punto A y el Punto B para
    establecer la ubicacion general de B respecto a A. Retorna uno de los
    nueve resultados definidos en la guia de la actividad.
    """
    if lat2 > lat1 and lon2 == lon1:
        return "Norte"
    elif lat2 < lat1 and lon2 == lon1:
        return "Sur"
    elif lat2 == lat1 and lon2 > lon1:
        return "Este"
    elif lat2 == lat1 and lon2 < lon1:
        return "Oeste"
    elif lat2 > lat1 and lon2 > lon1:
        return "Noreste"
    elif lat2 > lat1 and lon2 < lon1:
        return "Noroeste"
    elif lat2 < lat1 and lon2 > lon1:
        return "Sureste"
    elif lat2 < lat1 and lon2 < lon1:
        return "Suroeste"
    else:
        return "Misma ubicación"


def clasificar_distancia(distancia):
    """Clasifica la distancia (en km) segun los intervalos establecidos
    en la guia de la actividad, respetando los valores frontera.
    """
    if distancia < 1:
        return "Muy cercano"
    elif distancia < 10:
        return "Cercano"
    elif distancia < 50:
        return "Distancia media"
    else:
        return "Distante"


# ---------------------------------------------------------------------------
# Presentacion: construccion del informe, widget Text y ventanas emergentes.
# ---------------------------------------------------------------------------

def construir_informe(distancia, direccion, clasificacion):
    """Arma el texto del resultado con el mismo formato de la Actividad 01."""
    return "\n".join([
        LINEA,
        "RESULTADO DEL ANÁLISIS",
        LINEA,
        f"Distancia: {distancia:.3f} km",
        f"Dirección: {direccion}",
        f"Clasificación: {clasificacion}",
        LINEA,
    ])


def mostrar_resultado(area_texto, informe):
    """Reemplaza el contenido del widget Text por el informe indicado.
    Si el informe esta vacio, solo borra el resultado anterior.
    """
    area_texto.config(state="normal")
    area_texto.delete("1.0", tk.END)
    if informe:
        area_texto.insert("1.0", informe)
    area_texto.config(state="disabled")


def convertir_entradas(entradas):
    """Recupera con get() el contenido de las cuatro cajas de entrada y lo
    convierte a float. Lanza ValueError si algun campo esta vacio o no es
    un numero finito.
    """
    valores = []
    for caja in entradas:
        numero = float(caja.get().strip())
        if not math.isfinite(numero):  # rechaza 'nan' e 'inf'
            raise ValueError("valor no finito")
        valores.append(numero)
    return valores


def ejecutar_calculo(entradas, area_texto):
    """Callback del boton Calcular.

    Secuencia: 1) leer las cajas, 2) convertir a float (try/except),
    3) validar rangos, 4) calcular con las funciones de la Actividad 01 y
    5) reemplazar el resultado anterior en el widget Text.
    """
    try:
        lat_a, lon_a, lat_b, lon_b = convertir_entradas(entradas)
    except ValueError:
        mostrar_resultado(area_texto, "")
        messagebox.showerror(
            "Entrada no numérica",
            "Todos los campos deben contener valores numéricos.",
        )
        return

    if not (validar_coordenadas(lat_a, lon_a)
            and validar_coordenadas(lat_b, lon_b)):
        mostrar_resultado(area_texto, "")
        messagebox.showerror(
            "Coordenada fuera de rango",
            "La latitud debe estar entre -90 y 90 grados y la longitud "
            "entre -180 y 180 grados.",
        )
        return

    distancia = calcular_distancia(lat_a, lon_a, lat_b, lon_b)
    direccion = determinar_direccion(lat_a, lon_a, lat_b, lon_b)
    clasificacion = clasificar_distancia(distancia)

    mostrar_resultado(area_texto, construir_informe(distancia, direccion, clasificacion))


def limpiar_formulario(entradas, area_texto):
    """Vacia las cuatro cajas de entrada y el area de resultados."""
    for caja in entradas:
        caja.delete(0, tk.END)
    mostrar_resultado(area_texto, "")
    entradas[0].focus_set()


def crear_panel_punto(contenedor, titulo, columna):
    """Crea un recuadro (LabelFrame) con las cajas de latitud y longitud de
    un punto. Dentro del recuadro se usa unicamente grid().
    Retorna (caja_latitud, caja_longitud).
    """
    marco = ttk.LabelFrame(contenedor, text=titulo, padding=10)
    marco.grid(row=0, column=columna, padx=8, pady=4, sticky="nsew")

    ttk.Label(marco, text="Latitud").grid(row=0, column=0, sticky="w", padx=4, pady=4)
    caja_lat = ttk.Entry(marco, width=16)
    caja_lat.grid(row=0, column=1, padx=4, pady=4)

    ttk.Label(marco, text="Longitud").grid(row=1, column=0, sticky="w", padx=4, pady=4)
    caja_lon = ttk.Entry(marco, width=16)
    caja_lon.grid(row=1, column=1, padx=4, pady=4)

    return caja_lat, caja_lon


def construir_interfaz(ventana):
    """Construye la ventana principal. Retorna (entradas, area_texto), donde
    entradas = [latitud A, longitud A, latitud B, longitud B].
    """
    ventana.title("CTE-334 Análisis entre dos puntos geográficos")
    ventana.resizable(False, False)

    # Contenedor principal: se organiza solo con pack()
    principal = ttk.Frame(ventana, padding=12)
    principal.pack(fill="both", expand=True)

    ttk.Label(
        principal,
        text="CTE-334  Análisis entre dos puntos geográficos",
        font=("TkDefaultFont", 13, "bold"),
    ).pack(anchor="w", pady=(0, 4))

    ttk.Label(
        principal,
        text="Ingrese las coordenadas en grados decimales",
        font=("TkDefaultFont", 10, "bold"),
    ).pack(anchor="w", pady=(0, 6))

    # Marco con los dos puntos: se organiza solo con grid()
    marco_puntos = ttk.Frame(principal)
    marco_puntos.pack(fill="x")
    lat_a, lon_a = crear_panel_punto(marco_puntos, "Punto A", 0)
    lat_b, lon_b = crear_panel_punto(marco_puntos, "Punto B", 1)
    entradas = [lat_a, lon_a, lat_b, lon_b]

    # Area de resultados (solo lectura; se habilita al actualizarla)
    marco_resultado = ttk.LabelFrame(principal, text="Resultado", padding=10)
    area_texto = tk.Text(
        marco_resultado, width=44, height=7, font="TkFixedFont",
        state="disabled", relief="flat", bg="#f4f4f4",
    )
    area_texto.pack(fill="both", expand=True)

    # Botones (se crean aqui para que 'Calcular' y 'Limpiar' queden entre
    # los puntos y el resultado)
    marco_botones = ttk.Frame(principal)
    marco_botones.pack(pady=10)
    ttk.Button(
        marco_botones, text="Calcular",
        command=lambda: ejecutar_calculo(entradas, area_texto),
    ).pack(side="left", padx=6)
    ttk.Button(
        marco_botones, text="Limpiar",
        command=lambda: limpiar_formulario(entradas, area_texto),
    ).pack(side="left", padx=6)

    marco_resultado.pack(fill="both", expand=True, padx=8)

    # Enter equivale a presionar Calcular
    ventana.bind("<Return>", lambda evento: ejecutar_calculo(entradas, area_texto))
    lat_a.focus_set()

    return entradas, area_texto


def main():
    ventana = tk.Tk()
    construir_interfaz(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    main()
