import json
from pathlib import Path

RUTA_ARCHIVO_PRINCIPAL = Path(__file__).parent / "datos"


class Localidad:
    """Representa una localidad de un municipio, con su nombre y coordenadas geograficas."""

    def __init__(self, nombre, latitud, longitud):
        """
        Inicializa la localidad.
        :param nombre: Nombre de la localidad.
        :param latitud: Latitud de la localidad (None si no se conoce).
        :param longitud: Longitud de la localidad (None si no se conoce).
        """
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud

    def tiene_coordenadas(self):
        """
        Indica si la localidad tiene coordenadas registradas.
        :return: True si latitud y longitud no son None; False en caso contrario.
        """
        return self.latitud is not None and self.longitud is not None


class Municipio:
    """Representa un municipio que agrupa una lista de localidades."""

    def __init__(self, nombre):
        """
        Inicializa el municipio con su nombre y una lista vacia de localidades.
        :param nombre: Nombre del municipio.
        """
        self.nombre = nombre
        self.localidades = []

    def agregar_localidad(self, loc):
        """
        Agrega una localidad a la lista del municipio.
        :param loc: Objeto Localidad a agregar.
        """
        self.localidades.append(loc)

    def cantidad_total(self):
        """
        Devuelve la cantidad total de localidades del municipio.
        :return: Numero entero de localidades.
        """
        return len(self.localidades)

    def cantidad_con_coordenadas(self):
        """
        Cuenta las localidades del municipio que tienen coordenadas.
        :return: Numero de localidades con coordenadas.
        """
        contador = 0
        for loc in self.localidades:
            if loc.tiene_coordenadas():
                contador += 1
        return contador

    def cantidad_sin_coordenadas(self):
        """
        Cuenta las localidades del municipio que NO tienen coordenadas.
        :return: Numero de localidades sin coordenadas.
        """
        return self.cantidad_total() - self.cantidad_con_coordenadas()

    def porcentaje_con_coordenadas(self):
        """
        Calcula el porcentaje de localidades con coordenadas del municipio.
        :return: Porcentaje (float) redondeado a 2 decimales.
        """
        if self.cantidad_total() == 0:
            return 0
        return round(self.cantidad_con_coordenadas() / self.cantidad_total() * 100, 2)


class Main:
    """Se encarga de la carga de datos del archivo json y de mostrar el reporte."""

    def __init__(self, archivo):
        """
        Inicializa la clase.
        :param archivo: Nombre del archivo json a cargar.
        """
        self.archivo = archivo
        self.lista_municipios = []

    def cargar_datos(self):
        """
        Carga el archivo JSON y lo transforma en una lista de objetos Municipio,
        cada uno con su propia lista de objetos Localidad.
        """
        with open(RUTA_ARCHIVO_PRINCIPAL / self.archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        for nombre_muni in datos:
            municipio = Municipio(nombre_muni)
            for loc_dict in datos[nombre_muni]:
                loc = Localidad(loc_dict["localidad"], loc_dict["latitud"], loc_dict["longitud"])
                municipio.agregar_localidad(loc)
            self.lista_municipios.append(municipio)

    def mostrar_estadisticas(self):
        """
        Muestra el reporte de estadisticas POR CADA municipio:
        total de localidades, con y sin coordenadas, y porcentaje con coordenadas.
        """
        for municipio in self.lista_municipios:
            print(f"\n--- {municipio.nombre} ---")
            print(f"Localidades cargadas: {municipio.cantidad_total()}")
            print(f"Con coordenadas: {municipio.cantidad_con_coordenadas()}")
            print(f"Sin coordenadas: {municipio.cantidad_sin_coordenadas()}")
            print(f"Porcentaje con coordenadas: {municipio.porcentaje_con_coordenadas()}%")


main = Main("zonas_caracas.json")
main.cargar_datos()
main.mostrar_estadisticas()
