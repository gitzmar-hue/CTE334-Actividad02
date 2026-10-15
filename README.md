# CTE334-Actividad02

## 1. Datos del estudiante

- **Nombre:** Gitzy Yissel Andrade Andrade
- **Número de cuenta:** 20161030363
- **Curso:** CTE 334 – Desarrollo de Aplicaciones SIG (UNAH)

## 2. Propósito de la aplicación

Aplicación de escritorio con interfaz gráfica (Tkinter/ttk) que recibe las coordenadas en grados decimales de un Punto A y un Punto B, valida los datos y muestra dentro de la ventana la distancia (fórmula de Haversine), la dirección general de B respecto a A y la clasificación de la distancia. Es la conversión a interfaz gráfica del programa de la Actividad 01, reutilizando sus funciones.

## 3. Versión de Python y ejecución

- **Python:** 3.13 (probado con 3.13). Solo usa la biblioteca estándar (`math`, `tkinter`); no requiere instalar paquetes.
- **Ejecución:**

```bash
python actividad02.py
```

## 4. Controles principales de la interfaz

| Control | Función |
|---|---|
| Latitud / Longitud del Punto A | Cajas de entrada de las coordenadas del punto de origen |
| Latitud / Longitud del Punto B | Cajas de entrada de las coordenadas del punto de destino |
| Botón **Calcular** (o tecla Enter) | Valida las entradas y ejecuta el cálculo |
| Botón **Limpiar** | Vacía las cajas y el área de resultados |
| Área **Resultado** | Muestra el informe; cada cálculo reemplaza al anterior |

## 5. Caso propio: dos sitios reales de Honduras

| Dato | Valor |
|---|---|
| Punto A: San Pedro Sula | 15.5042, -88.0250 |
| Punto B: La Ceiba | 15.7835, -86.7933 |

Resultado mostrado en la ventana:

```
----------------------------------------
RESULTADO DEL ANÁLISIS
----------------------------------------
Distancia: 135.493 km
Dirección: Noreste
Clasificación: Distante
----------------------------------------
```

## 6. Decisiones de interfaz

Separé la lógica de la presentación: las cuatro funciones de la Actividad 01 no conocen widgets ni ventanas emergentes, y solo `ejecutar_calculo()` las conecta con la interfaz. La conversión a `float` se hace dentro de `try/except` antes de comparar rangos, de modo que un texto como "abc" muestra «Entrada no numérica» y no se confunde con «Coordenada fuera de rango». Además, rechazo valores como `nan` o `inf`, y en ambos errores se borra el resultado anterior para no dejar a la vista un cálculo que ya no corresponde a las entradas.

## Pruebas realizadas

| Caso | Entradas | Resultado |
|---|---|---|
| A | Tegucigalpa (14.0723, -87.1921) y Comayagua (14.4514, -87.6375) | 63.882 km; Noroeste; Distante |
| B | Dos puntos idénticos | 0.000 km; Misma ubicación; Muy cercano |
| C | Campo vacío o `abc` | Ventana «Entrada no numérica» |
| D | Latitud 97.5 | Ventana «Coordenada fuera de rango» |
| E | Longitud -185 | Ventana «Coordenada fuera de rango» |
| F | San Pedro Sula y La Ceiba | 135.493 km; Noreste; Distante |

Los valores límite -90, 90, -180 y 180 se aceptan como válidos.
