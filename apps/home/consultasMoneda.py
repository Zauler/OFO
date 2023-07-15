import requests
from os import getenv
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
MONEDAS_API = getenv("MONEDAS_API")


class Monedas():

    def consulta_api():
        API = "16675157b671a5ebe69d2597fe498406"
        url = f"http://api.exchangeratesapi.io/v1/latest?access_key={MONEDAS_API}"
        #url = "https://api.ejemplo.com/endpoint"  # Reemplaza con la URL de la API que deseas consultar

        try:
            response = requests.get(url)
            response.raise_for_status()  # Lanza una excepción si la respuesta tiene un código de error
            data = response.json()  # Convierte la respuesta JSON en un objeto Python
            # Aquí puedes realizar acciones con los datos de la API o devolverlos en la respuesta de Flask
            return data['rates']
        except requests.exceptions.RequestException as e:
            # Maneja los errores de solicitud, como errores de conexión o tiempo de espera agotado
            return "Error: " + str(e)