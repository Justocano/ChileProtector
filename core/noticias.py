import requests

from datetime import datetime, timedelta
from .integracion import obtener_nombre_comuna
def obtener_noticias(comuna_id):
    # Fecha del día actual
    fecha_actual = datetime(2024, 8, 23)

    # Calcular la fecha de un mes atrás (aproximadamente 30 días)
    fecha_mes_atras = fecha_actual - timedelta(days=30)

    # Formatear las fechas en el formato 'YYYY-MM-DD'
    fecha_actual_str = fecha_actual.strftime('2024-11-10')
    fecha_mes_atras_str = fecha_mes_atras.strftime('2024-12-10')
    nombre = obtener_nombre_comuna(comuna_id)
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': f'crimen&{nombre}',  # Búsqueda de "crimen" y el nombre de la comuna
        'from': fecha_mes_atras_str,  
        'to': fecha_actual_str,
        'sortBy': 'publishedAt',
        'apiKey': 'a831a26a34644ef3973070fedbc6375b'
    }

    response = requests.get(url, params=params)
    data = response.json()

    articles = data.get('articles', [])
    print(articles)
    return articles

