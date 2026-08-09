# Para poder leer archivos json
# Librerias nativas
import json
from pathlib import Path

# Librerias de terceros 
import requests

# CONSTANTES
RUTA_ARCHIVO_PRINCIPAL = Path(__file__).parent / "datos"
URL_API = "https://api.open-meteo.com/v1/forecast"
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
    83: "Chubascos de nieve ligera",
    84: "Chubascos de nieve moderada",
    85: "Chubascos de nieve intensa",
    86: "Chubascos de aguanieve",
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
    
    def mostrar_menu(self):
        """
        Muestra el menu principal.
        """
        while self.activo:
            print("\n-----> MENÚ PRINCIPAL <-----")
            print("1.- Seleccionar un municipio y su localidad")
            print("2.- Ver estadisticas de los municipios y localidades")
            print("3.- Salir")
            opcion = input("\nElige una opcion: ")
            
            if opcion == "1":
                self.seleccionar_municipio()
            elif opcion == "2":
                self.mostrar_estadisticas()
            elif opcion == "3":
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
        Imprime las estadisticas de los datos cargados.
        """
        print(f"Cantidad de municipios: {self.cantidad_municipios}")
        print(f"Cantidad de localidades: {self.cant_loc_con_coordenadas + self.cant_loc_sin_coordenadas}")
        print(f"Cantidad de localidades con coordenadas: {self.cant_loc_con_coordenadas}")
        print(f"Cantidad de localidades sin coordenadas: {self.cant_loc_sin_coordenadas}")
        print(f"Porcentaje de localidades con coordenadas: {self.porc_loc_con_coordenadas}%")
        print(f"Porcentaje de localidades sin coordenadas: {self.porc_loc_sin_coordenadas}%")

    def seleccionar_municipio(self):
        """
        Selecciona un municipio de la lista de municipios.
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
        
        for i, localidad in enumerate(self.lista_localidades):
            if localidad.municipio == self.lista_municipios[eleccion - 1]:
                if localidad.longitud is not None and localidad.latitud is not None:
                    print(f"{i + 1}. {localidad.nombre}")
        eleccion2 = input("\nSeleccione una localidad: ")
        if not eleccion2.isdigit():
            print("Error: Por favor, ingrese un número.")
            return None
        eleccion2 = int(eleccion2)
        if eleccion2 < 1 or eleccion2 > len(self.lista_localidades):
            print("Error: El número seleccionado no es válido.")
            return None
        localidad_seleccionada = self.lista_localidades[eleccion2 - 1]
        # print(f"Localidad: {localidad_seleccionada.nombre}")
        # print(f"Latitud: {localidad_seleccionada.latitud}")
        # print(f"Longitud: {localidad_seleccionada.longitud}")
        print("\n-----> DATOS DEL CLIMA <-----\n")
        print(self.obtener_clima(localidad_seleccionada))

    def obtener_clima(self, localidad):
        """
        Obtiene los datos del clima de la localidad desde la API de Open-Meteo.
        :param localidad: Localidad de la cual se quieren obtener los datos. 
        :return: String con el clima de la localidad. None si hay error.
        """
        url = URL_API + f"?latitude={localidad.latitud}&longitude={localidad.longitud}&current=weather_code"
        respuesta = requests.get(url)
        datos = respuesta.json()
        if datos.get("error"):
            print("Error: No se pudieron obtener los datos del clima.")
            return None
        clima = WEATHER_CODE.get(datos.get("current").get("weather_code")) 
        return f"Clima en {localidad.nombre}: {clima}"

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

# Crear un objeto de la clase Main
main = Main("zonas_caracas.json")

# Cargar los datos
main.cargar_datos()

# Mostrar las estadisticas
main.mostrar_estadisticas()

# Ejecutar el menu
main.mostrar_menu()