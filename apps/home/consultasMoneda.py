import requests
import datetime
import json
from os import getenv
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
MONEDAS_API = getenv("MONEDAS_API")


class Monedas():
    def __init__(self):
        self.ultimo_instante = None

    def consulta_api(self):
        # Verificar si ha pasado 1 hora desde la última consulta
        if self.ha_pasado_una_hora():
            url = f"http://api.exchangeratesapi.io/v1/latest?access_key={MONEDAS_API}"

            print ("HA CONSULTADO")

            try:
                response = requests.get(url)
                response.raise_for_status()  # Lanza una excepción si la respuesta tiene un código de error
                data = response.json()  # Convierte la respuesta JSON en un objeto Python

                # Actualizar el último instante con el valor actual
                self.ultimo_instante = datetime.datetime.now()

                with open("././datos/consultamoneda.json", "w") as archivo_json:
                    json.dump(data['rates'], archivo_json)

                return data['rates']
            except requests.exceptions.RequestException as e:
                # Maneja los errores de solicitud, como errores de conexión o tiempo de espera agotado
                return "Error: " + str(e)
        else:
            with open("././datos/consultamoneda.json", "r") as archivo_json:
                datos_cargados = json.load(archivo_json)

            print("No ha pasado 1 hora desde la última consulta. Espere un poco más.")
            return datos_cargados
           

    # Función para comprobar si ha pasado 1 hora desde la última consulta
    def ha_pasado_una_hora(self):
        print ("dentro")
        if not self.ultimo_instante:
            return True
        instante_actual = datetime.datetime.now()
        diferencia = instante_actual - self.ultimo_instante

        print ("DIFERENCIA: ",diferencia.total_seconds())
        print ("ULTIMO INSTANTE: ", self.ultimo_instante)
        return diferencia.total_seconds() >= 3600