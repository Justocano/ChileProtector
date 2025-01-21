import requests
import urllib3
import unicodedata
# Desactivar advertencias de solicitudes inseguras
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def obtener_comunas():
    url = 'https://localhost:44381/api/Comunas'
    
    try:
        response = requests.get(url, verify=False)  # Desactivar la verificación SSL
        response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa
        comunas = response.json()  # Convertir la respuesta a JSON
        return comunas
    except requests.exceptions.RequestException as e:
        # Manejar errores de solicitud
        print(f"Error al obtener comunas: {e}")
        return None

def obtener_regiones():
    url = 'https://localhost:44381/api/Regiones'
    
    try:
        response = requests.get(url, verify=False)  # Desactivar la verificación SSL
        response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa
        comunas = response.json()  # Convertir la respuesta a JSON
        return comunas
    except requests.exceptions.RequestException as e:
        # Manejar errores de solicitud
        print(f"Error al obtener regiones: {e}")
        return None

def obtener_comuna(comuna_id):
    url = f'https://localhost:44381/api/Comunas/{comuna_id}'

    try:
        response = requests.get(url, verify=False)  # Desactivar la verificación SSL
        response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa
        comuna = response.json()  # Convertir la respuesta a JSON
        return comuna
    except requests.exceptions.RequestException as e:
        # Manejar errores de solicitud
        print(f"Error al obtener la comuna: {e}")
        return None

def obtener_nombre_comuna(comuna_id):
    url = f'https://localhost:44381/api/Comunas/{comuna_id}'
    
    try:
        response = requests.get(url, verify=False)  # Desactivar la verificación SSL
        response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa
        comuna = response.json()  # Convertir la respuesta a JSON

        # Retornar solo el nombre de la comuna
        nombre_comuna = comuna.get('nombre', None)  # Asumiendo que la clave es 'nombre'
        return nombre_comuna

    except requests.exceptions.RequestException as e:
        # Manejar errores de solicitud
        print(f"Error al obtener la comuna: {e}")
        return None

def obtener_region(region_id):
    url = f'https://localhost:44381/api/Regiones/{region_id}'

    try:
        response = requests.get(url, verify=False)  # Desactivar la verificación SSL
        response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa
        comuna = response.json()  # Convertir la respuesta a JSON
        return comuna
    except requests.exceptions.RequestException as e:
        # Manejar errores de solicitud
        print(f"Error al obtener la region: {e}")
        return None


def normalizar_cadena(cadena):
    return unicodedata.normalize('NFKD', cadena).encode('ascii', 'ignore').decode('ascii').lower()

def buscar_comunas_por_nombre(nombre_comuna):
    comunas = obtener_comunas()
    if comunas is None:
        return []
    
    nombre_comuna = normalizar_cadena(nombre_comuna)  # Normalizar y convertir a minúsculas
    comunas_filtradas = [comuna for comuna in comunas if nombre_comuna in normalizar_cadena(comuna.get('nombre', ''))]
    
    return comunas_filtradas