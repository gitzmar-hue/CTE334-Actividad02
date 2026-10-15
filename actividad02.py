"""
CTE-334 - Desarrollo de Aplicaciones SIG
Actividad 02 - Distancia y direccion con interfaz grafica
Autor: Gitzy Yissel Andrade Andrade
Numero de cuenta: 20161030363
"""

import tkinter as tk
from tkinter import ttk



# ---------------------------------------------------------------------------
# Etapa 1: solo la interfaz. El boton Calcular aun no procesa datos.
# ---------------------------------------------------------------------------

def mostrar_resultado(area_texto, informe):
    """Reemplaza el contenido del widget Text por el informe indicado."""
    area_texto.config(state="normal")
    area_texto.delete("1.0", tk.END)
    if informe:
        area_texto.insert("1.0", informe)
    area_texto.config(state="disabled")


def ejecutar_calculo(entradas, area_texto):
    """Callback provisional del boton Calcular (se conectara en la etapa 2)."""
    mostrar_resultado(area_texto, "Cálculo pendiente de conectar.")


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
