# Para poder leer archivos json
import json
from pathlib import Path
import requests


# CONSTANTE
RUTA_ARCHIVO_PRINCIPAL = Path(__file__).parent / "datos"
WEATHER_CODE = {
    0: "Despejado",
    1: "Mayormente despejado",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Niebla",
    48: "Niebla con escarcha",
    51: "Llovizna ligera",
    53: "Llovizna moderada",
    55: "Llovizna intensa",
    56: "Llovizna ligera helada",
    57: "Llovizna intensa helada",
    61: "Lluvia ligera",
    63: "Lluvia moderada",
    65: "Lluvia intensa",
    66: "Lluvia ligera helada",
    67: "Lluvia intensa helada",
    71: "Nieve ligera",
    73: "Nieve moderada",
    75: "Nieve intensa",
    77: "Granos de hielo",
    80: "Chubascos de lluvia ligera",
    81: "Chubascos de lluvia moderada",
    82: "Chubascos de lluvia intensa",
    85: "Chubascos de nieve ligera",
    86: "Chubascos de nieve intensa",
    95: "Tormenta eléctrica",
    96: "Tormenta eléctrica con granizo ligero",
    99: "Tormenta eléctrica con granizo intenso"
}





# Definir las clases
class Main:
    """
    Esta clase se encarga de la carga de datos de un archivo json, el manejo de los datos y la ejecucion del programa.
    """
    def __init__(self, archivo):
        """
        Inicializa la clase.
        :param archivo: Ruta del archivo json a cargar.
        """
        self.archivo = archivo
        self.lista_municipios = []
        self.lista_localidades = []
        self.cantidad_municipios = 0
        self.cant_loc_sin_coordenadas = 0
        self.cant_loc_con_coordenadas = 0
        self.porc_loc_sin_coordenadas = 0
        self.porc_loc_con_coordenadas = 0
        self.activo = True
        self.consultas = []
    
    def mostrar_menu(self):
        """
        Muestra el menu principal y ejecuta la opcion elegida por el usuario.
        """
        while self.activo:
            print("\n-----> MENÚ PRINCIPAL <-----")
            print("1.- Seleccionar un municipio y su localidad")
            print("2.- Buscar localidad por nombre")
            print("3.- Ver estadisticas de los municipios y localidades")
            print("4.- Ver cobertura (localidades sin coordenadas)")
            print("5.- Ranking de temperatura (sesion)")
            print("6.- Promedio de temperatura (sesion)")
            print("7.- Salir")
            opcion = input("\nElige una opcion: ")
            if opcion == "1":
                self.seleccionar_municipio()
            elif opcion == "2":
                self.buscar_por_nombre()
            elif opcion == "3":
                self.mostrar_estadisticas()
            elif opcion == "4":
                self.mostrar_cobertura()
            elif opcion == "5":
                self.mostrar_ranking()
            elif opcion == "6":
                self.mostrar_promedio()
            elif opcion == "7":
                self.salir()
            else:
                print("Opción no válida. Intenta de nuevo.")
    
    def salir(self):
        """
        Sale del programa.
        """
        self.activo = False
        print("Saliendo del programa...")

    def cargar_datos(self):
        """
        Carga los datos del archivo json y los guarda en la lista de municipios.
        Genera las estadisticas de los datos cargados.
        """
        with open(RUTA_ARCHIVO_PRINCIPAL / self.archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        for municipio in datos:
            for localidad in datos[municipio]:
                if localidad['longitud'] is None or localidad['latitud'] is None:
                    self.lista_localidades.append(Localidad(localidad['localidad'], municipio, None, None))
                    self.cant_loc_sin_coordenadas += 1
                else:
                    self.lista_localidades.append(Localidad(localidad['localidad'], municipio, localidad['longitud'], localidad['latitud']))
                    self.cant_loc_con_coordenadas += 1
            self.lista_municipios.append(municipio)
        self.cantidad_municipios = len(set(self.lista_municipios))
        self.porc_loc_sin_coordenadas = round((self.cant_loc_sin_coordenadas / (self.cant_loc_con_coordenadas + self.cant_loc_sin_coordenadas)) * 100, 2)
        self.porc_loc_con_coordenadas = round((self.cant_loc_con_coordenadas / (self.cant_loc_con_coordenadas + self.cant_loc_sin_coordenadas)) * 100, 2)

    def devolver_lista_municipios(self):
        """
        Devuelve la lista de municipios.
        """
        return self.lista_municipios

    def devolver_lista_localidades(self):
        """
        Devuelve la lista de localidades.
        """
        return self.lista_localidades

    def devolver_estadisticas(self):
        """
        Devuelve las estadisticas de los datos cargados.
        """
        return self.cantidad_municipios, self.cant_loc_sin_coordenadas, self.cant_loc_con_coordenadas

    def imprimir_datos(self):
        """
        Imprime los datos cargados.
        """
        for localidad in self.lista_localidades:
            print(f"Municipio: {localidad.municipio}, Localidad: {localidad.nombre}, Coordenadas: ({localidad.longitud}, {localidad.latitud})")

    def mostrar_estadisticas(self):
        """
        Muestra las estadisticas POR CADA municipio: total de localidades,
        con y sin coordenadas, y porcentaje con coordenadas.
        """
        for nombre_municipio in self.lista_municipios:
            total = 0
            con_coordenadas = 0
            for localidad in self.lista_localidades:
                if localidad.municipio == nombre_municipio:
                    total += 1
                    if localidad.longitud is not None and localidad.latitud is not None:
                        con_coordenadas += 1
            sin_coordenadas = total - con_coordenadas
            if total > 0:
                porcentaje = round(con_coordenadas / total * 100, 2)
            else:
                porcentaje = 0
            print(f"\n--- {nombre_municipio} ---")
            print(f"Localidades cargadas: {total}")
            print(f"Con coordenadas: {con_coordenadas}")
            print(f"Sin coordenadas: {sin_coordenadas}")
            print(f"Porcentaje con coordenadas: {porcentaje}%")
            
    def seleccionar_municipio(self):
        """
        Selecciona un municipio y una de sus localidades con coordenadas,
        y muestra el clima de la localidad elegida.
        """
        for i, municipio in enumerate(self.lista_municipios):
            print(f"{i + 1}. {municipio}")
        eleccion = input("\nSeleccione un municipio: ")
        if not eleccion.isdigit():
            print("Error: Por favor, ingrese un número.")
            return None
        eleccion = int(eleccion)
        if eleccion < 1 or eleccion > len(self.lista_municipios):
            print("Error: El número seleccionado no es válido.")
            return None
        municipio_elegido = self.lista_municipios[eleccion - 1]

        
        localidades_municipio = []
        for localidad in self.lista_localidades:
            if localidad.municipio == municipio_elegido:
                if localidad.longitud is not None and localidad.latitud is not None:
                    localidades_municipio.append(localidad)

        
        for i, localidad in enumerate(localidades_municipio):
            print(f"{i + 1}. {localidad.nombre}")

        eleccion2 = input("\nSeleccione una localidad: ")
        if not eleccion2.isdigit():
            print("Error: Por favor, ingrese un número.")
            return None
        eleccion2 = int(eleccion2)
        if eleccion2 < 1 or eleccion2 > len(localidades_municipio):
            print("Error: El número seleccionado no es válido.")
            return None
        localidad_seleccionada = localidades_municipio[eleccion2 - 1]

        print(f"Localidad: {localidad_seleccionada.nombre}")
        print(f"Latitud: {localidad_seleccionada.latitud}")
        print(f"Longitud: {localidad_seleccionada.longitud}")
        datos = self.obtener_datos_api(localidad_seleccionada)
        print(datos)
        
    def obtener_datos_api(self, localidad):
        """
        Consulta el clima actual de una localidad en la API de Open-Meteo.
        :param localidad: Objeto Localidad con latitud y longitud.
        :return: Un texto con el clima, o un mensaje de error si falla la conexion.
        """
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": localidad.latitud,
            "longitude": localidad.longitud,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        }
        try:
            respuesta = requests.get(url, params=params, timeout=15)
            datos = respuesta.json()

            actual = datos["current"]
            temperatura = actual["temperature_2m"]
            self.consultas.append(Clima(localidad.nombre, localidad.municipio, temperatura))
            humedad = actual["relative_humidity_2m"]
            viento = actual["wind_speed_10m"]
            codigo = actual["weather_code"]
            estado = WEATHER_CODE.get(codigo, "Desconocido")

            texto = (f"Municipio: {localidad.municipio}\n"
                     f"Localidad: {localidad.nombre}\n"
                     f"Coordenadas: ({localidad.latitud}, {localidad.longitud})\n"
                     f"Temperatura: {temperatura} C\n"
                     f"Humedad: {humedad}%\n"
                     f"Viento: {viento} km/h\n"
                     f"Estado del tiempo: {estado}")
            return texto
        except requests.RequestException:
            return "Error: no se pudo conectar con la API del clima. Revisa tu internet."
        
    
    def buscar_por_nombre(self):
        """
        Busca localidades por nombre (o parte del nombre) y muestra el clima
        de la que elija el usuario.
        """
        texto = input("\nEscriba el nombre (o parte) de la localidad: ")
        coincidencias = []
        for localidad in self.lista_localidades:
            if texto.lower() in localidad.nombre.lower():      
                if localidad.longitud is not None and localidad.latitud is not None:
                    coincidencias.append(localidad)

        if len(coincidencias) == 0:
            print("No se encontraron localidades con ese nombre.")
            return None

        for i, localidad in enumerate(coincidencias):
            print(f"{i + 1}. {localidad.nombre} ({localidad.municipio})")

        eleccion = input("\nSeleccione una localidad: ")
        if not eleccion.isdigit():
            print("Error: Por favor, ingrese un numero.")
            return None
        eleccion = int(eleccion)
        if eleccion < 1 or eleccion > len(coincidencias):
            print("Error: El numero seleccionado no es valido.")
            return None
        localidad_seleccionada = coincidencias[eleccion - 1]
        print(self.obtener_datos_api(localidad_seleccionada))
        
    def mostrar_cobertura(self):
        """
        Muestra las localidades SIN coordenadas, agrupadas por municipio.
        """
        for nombre_municipio in self.lista_municipios:
            print(f"\n--- {nombre_municipio} (sin coordenadas) ---")
            for localidad in self.lista_localidades:
                if localidad.municipio == nombre_municipio:
                    if localidad.longitud is None or localidad.latitud is None:
                        print(f"- {localidad.nombre}")
                        
    def mostrar_ranking(self):
        """
        Muestra la localidad mas calida y la mas fria de las consultadas en la sesion.
        """
        if len(self.consultas) == 0:
            print("Aun no has consultado ninguna localidad en esta sesion.")
            return None
        mas_calida = self.consultas[0]
        mas_fria = self.consultas[0]
        for c in self.consultas:
            if c.temperatura > mas_calida.temperatura:
                mas_calida = c
            if c.temperatura < mas_fria.temperatura:
                mas_fria = c
        print(f"Mas calida: {mas_calida.localidad} ({mas_calida.municipio}) - {mas_calida.temperatura} C")
        print(f"Mas fria: {mas_fria.localidad} ({mas_fria.municipio}) - {mas_fria.temperatura} C")

    def mostrar_promedio(self):
        """
        Muestra el promedio de temperatura de las localidades consultadas en la sesion.
        """
        if len(self.consultas) == 0:
            print("Aun no has consultado ninguna localidad en esta sesion.")
            return None
        suma = 0
        for c in self.consultas:
            suma += c.temperatura
        promedio = round(suma / len(self.consultas), 2)
        print(f"Promedio de {len(self.consultas)} consultas: {promedio} C")
    
    
    
    
    


# class Municipio:
#     """
#     Esta clase se encarga de almacenar los datos de un municipio.
#     """
#     def __init__(self, nombre, localidades):
#         """
#         Inicializa la clase.
#         :param nombre: Nombre del municipio.
#         :param localidades: Lista de localidades del municipio.
#         """
#         self.nombre = nombre
#         self.localidades = localidades

class Localidad:
    """
    Esta clase se encarga de almacenar los datos de una localidad.
    """
    def __init__(self, nombre, municipio, longitud, latitud):
        """
        Inicializa la clase.
        :param nombre: Nombre de la localidad.
        :param municipio: Municipio al que pertenece la localidad.
        :param longitud: Longitud de la localidad.
        :param latitud: Latitud de la localidad.
        """
        self.nombre = nombre
        self.municipio = municipio
        self.longitud = longitud
        self.latitud = latitud
        
        
        
        
        
        
class Clima:
    """Guarda el resultado de una consulta de clima hecha en la sesion."""
    def __init__(self, localidad, municipio, temperatura):
        """
        Inicializa una consulta de clima.
        :param localidad: Nombre de la localidad.
        :param municipio: Municipio de la localidad.
        :param temperatura: Temperatura consultada.
        """
        self.localidad = localidad
        self.municipio = municipio
        self.temperatura = temperatura
               

# Crear un objeto de la clase Main
main = Main("zonas_caracas.json")

# Cargar los datos
main.cargar_datos()

# Mostrar las estadisticas
main.mostrar_estadisticas()

# Ejecutar el menu
main.mostrar_menu()

# Seleccionar un municipio
# municipio = main.seleccionar_municipio()