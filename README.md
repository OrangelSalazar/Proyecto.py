# MeteoCaracas

Sistema de monitoreo y consulta del clima del Área Metropolitana de Caracas,
desarrollado en Python bajo el enfoque de Programación Orientada a Objetos (POO).

Los datos meteorológicos se obtienen en tiempo real de la API pública de Open-Meteo.

---

##  Descripción

MeteoCaracas permite:

- Consultar el clima actual de las localidades de los 5 municipios de Caracas
  (Chacao, Baruta, El Hatillo, Sucre y Libertador).
- Ver estadísticas de cobertura geográfica (localidades con y sin coordenadas).
- Consultar el ranking y el promedio de temperatura de la sesión.
- Consultar datos históricos por año y visualizarlos en un gráfico.

---

##  Requisitos

- **Python 3.10** o superior
- Conexión a **internet** (para consultar la API del clima)

---

##  Instalación

Instala las librerías necesarias:

```bash
pip install requests matplotlib
```

---

##  Cómo ejecutar

1. Asegúrate de que exista una carpeta `datos` con el archivo
   `zonas_caracas.json` dentro, ubicada junto al `app.py`:

   ```
   Proyecto.py/
   ├── app.py
   └── datos/
       └── zonas_caracas.json
   ```

2. Ejecuta el programa:

   ```bash
   python app.py
   ```

3. Al iniciar se muestra un reporte de estadísticas por municipio y luego el menú principal.

---

##  Funcionalidades (menú principal)

| Opción | Descripción |
|--------|-------------|
| 1 | **Seleccionar municipio y localidad** → muestra el clima actual (temperatura, humedad, viento y estado). |
| 2 | **Buscar localidad por nombre** → filtra por coincidencias y muestra el clima. |
| 3 | **Ver estadísticas** → localidades por municipio, con/sin coordenadas y porcentaje. |
| 4 | **Ver cobertura** → lista las localidades sin coordenadas, agrupadas por municipio. |
| 5 | **Ranking de temperatura** → localidad más cálida y más fría de la sesión. |
| 6 | **Promedio de temperatura** → promedio de las localidades consultadas en la sesión. |
| 7 | **Ver histórico** → datos por año en un rango de fechas + gráfico con Matplotlib. |
| 8 | **Salir** |

---

## Estructura de clases (POO)

- **`Main`** → carga los datos del JSON, gestiona el menú y coordina todo el programa.
- **`Localidad`** → almacena el nombre, municipio y coordenadas (latitud/longitud) de cada localidad.
- **`Clima`** → guarda el resultado de cada consulta de clima hecha durante la sesión
  (para el ranking y el promedio).
- **`ResumenAnual`** → guarda el resumen (temperatura, precipitación y viento) de cada año
  en la consulta de datos históricos.

---

## Librerías utilizadas

- **`requests`** → consultar las APIs de Open-Meteo.
- **`matplotlib`** → generar los gráficos de datos históricos.
- **`json`** → leer el archivo de datos (nativa de Python).
- **`pathlib`** → manejar la ruta del archivo (nativa de Python).
- **`os`** → habilitar los colores en la consola (nativa de Python).

---

## APIs utilizadas

- **Clima actual:** `https://api.open-meteo.com/v1/forecast`
- **Datos históricos:** `https://archive-api.open-meteo.com/v1/archive`

---

## Integrantes

- Steven Méndez
- Orangel Salazar
- Gabriel Urdaneta

---
*Proyecto desarrollado para la asignatura **Algoritmos y Programación** — Universidad Metropolitana.*

