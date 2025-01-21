import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import  Servicio,Comuna,Categoria,Perfil
# Carrito, Perfil, Boleta, DetalleBoleta, Bodega, 

def eliminar_tabla(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='123')
            usuario.is_user=False
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='123')
            usuario.is_user=True

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    #eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    # eliminar_tabla('Bodega')
    # eliminar_tabla('DetalleBoleta')
    # eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    # eliminar_tabla('Carrito')
    # eliminar_tabla('Producto')
    eliminar_tabla('Servicio')
    # eliminar_tabla('Categoria')
    # eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd():
    eliminar_tablas()
    print('tablas eliminadas')
    crear_usuario(
        username='cevans',
        tipo='Cliente', 
        nombre='Chris', 
        apellido='Evans', 
        correo='cevans@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='15499707-3', 
        direccion='123 Main Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/cevans.jpg')

    crear_usuario(
        username='eolsen',
        tipo='Cliente', 
        nombre='Elizabeth', 
        apellido='Olsen', 
        correo='eolsen@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='19090011-2', 
        direccion='Albert Street, New York, \nNew York 10001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/eolsen.jpg')

    crear_usuario(
        username='tholland',
        tipo='Cliente', 
        nombre='Tom', 
        apellido='Holland', 
        correo='tholland@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='23548549-0', 
        direccion='105 Apple Park Way, \nCupertino, CA 95014 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/tholland.jpg')

    crear_usuario(
        username='sjohansson',
        tipo='Cliente', 
        nombre='Scarlett', 
        apellido='Johansson', 
        correo='sjohansson@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='12788999-4', 
        direccion='350 5th Ave, \nNew York, NY 10118 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/sjohansson.jpg')

    crear_usuario(
        username='admin',
        tipo='Administrador', 
        nombre='admin', 
        apellido='', 
        correo='admin@marvel.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='16543210-8', 
        direccion='10 Pine Road, Miami, \nFlorida 33101 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/cpratt.jpg')
    
    crear_usuario(
        username='mruffalo',
        tipo='Administrador', 
        nombre='Mark', 
        apellido='Ruffalo', 
        correo='mruffalo@marvel.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='21123344-7', 
        direccion='1600 Pennsylvania Avenue NW, \nWashington, D.C. \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/mruffalo.jpg')

    crear_usuario(
        username='super',
        tipo='Superusuario',
        nombre='Robert',
        apellido='Downey Jr.',
        correo='rdowneyjr@marvel.com',
        es_superusuario=True,
        es_staff=True,
        rut='18472636-6',
        direccion='15 Oak Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos',
        subscrito=False,
        imagen='perfiles/rdowneyjr.jpg')
    
    # categorias_data = [
    #     { 'id':1, 'nombre': 'autos'},
    #     { 'id':2, 'nombre': 'motos'},
    #     { 'id':3, 'nombre': 'bicicletas'},
    #     { 'id':4, 'nombre': 'aviones'}
    # ]

    # print('Crear categorías')
    # for categoria in categorias_data:
    #     Categoria.objects.create(**categoria)
    # print('Categorías creadas correctamente')
    

    # comunas = [
    #     {
    #         # "id": 1,
    #         "nombre": "Santiago",
    #         "descripcion": "Santiago es la capital de Chile, conocida por su rica historia, arquitectura colonial y vibrante vida cultural. Lugares emblemáticos incluyen la Plaza de Armas, el Cerro Santa Lucía y el Palacio de La Moneda.",
    #         "imagen": "Comunas/Santiago.jpg",
    #         "Clase": "Comuna Poco Segura"
    #     },
    #     {
    #         # "id": 2,
    #         "nombre": "Providencia",
    #         "descripcion": "Providencia es una comuna residencial y comercial de Santiago, famosa por su diversidad gastronómica, el Parque Metropolitano (Cerro San Cristóbal) y el Barrio Bellavista.",
    #         "imagen": "Comunas/Providencia.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 3,
    #         "nombre": "Las Condes",
    #         "descripcion": "Las Condes es una comuna elegante y moderna de Santiago, reconocida por sus centros comerciales, parques urbanos y una vida nocturna animada. Lugares destacados incluyen el Parque Araucano y el Mall Parque Arauco.",
    #         "imagen": "Comunas/Las Condes.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 4,
    #         "nombre": "Maipú",
    #         "descripcion": "Maipú es una comuna con una rica historia y cultura, conocida por su Plaza de Maipú, la Viña Undurraga y el Templo Votivo de Maipú, un monumento nacional.",
    #         "imagen": "Comunas/Maipú.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 5,
    #         "nombre": "Vitacura",
    #         "descripcion": "Vitacura es una comuna elegante y exclusiva de Santiago, con lujosas boutiques, galerías de arte y hermosos parques como el Parque Bicentenario.",
    #         "imagen": "Comunas/Vitacura.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 6,
    #         "nombre": "Ñuñoa",
    #         "descripcion": "Ñuñoa es una comuna con un ambiente bohemio y cultural, hogar de la Universidad de Chile y el Estadio Nacional. El Barrio Italia es conocido por sus tiendas de diseño y cafés.",
    #         "imagen": "Comunas/Ñuñoa.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 7,
    #         "nombre": "La Reina",
    #         "descripcion": "La Reina es una comuna residencial conocida por sus parques, como el Parque Mahuida y el Parque Padre Hurtado. También alberga la Iglesia de La Reina, un sitio de interés cultural.",
    #         "imagen": "Comunas/La Reina.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 8,
    #         "nombre": "Puente Alto",
    #         "descripcion": "Puente Alto es una comuna con una gran oferta comercial y recreativa, destacando el Santuario de la Naturaleza el Arrayán y el Mall Plaza Tobalaba. Es una de las comunas más pobladas de Santiago.",
    #         "imagen": "Comunas/Puente Alto.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 9,
    #         "nombre": "Quinta Normal",
    #         "descripcion": "Quinta Normal es conocida por su parque del mismo nombre, que alberga el Museo Nacional de Historia Natural, el Museo de Arte Contemporáneo y el Jardín Botánico. También es sede de la Feria Internacional del Libro de Santiago.",
    #         "imagen": "Comunas/Quinta Normal.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 10,
    #         "nombre": "Recoleta",
    #         "descripcion": "Recoleta es una comuna con una rica historia, destacando la Iglesia de Recoleta Dominica, el Cerro Blanco y el Cementerio General de Santiago, uno de los más grandes de América Latina.",
    #         "imagen": "Comunas/Recoleta.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 11,
    #         "nombre": "Renca",
    #         "descripcion": "Renca es una comuna en crecimiento, con una mezcla de zonas residenciales e industriales. Destacan el Parque Mapocho Poniente y el Parque Cerro Chena para actividades al aire libre.",
    #         "imagen": "Comunas/Renca.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 12,
    #         "nombre": "San Bernardo",
    #         "descripcion": "San Bernardo es una comuna al sur de Santiago, conocida por sus viñedos y actividades agrícolas. También cuenta con el Parque Safari y el Parque El Pueblito, un centro recreativo.",
    #         "imagen": "Comunas/San Bernardo.jpg",
    #         "Clase": "Comuna rural"
    #     },
    #     {
    #         # "id": 13,
    #         "nombre": "San Miguel",
    #         "descripcion": "San Miguel es una comuna residencial con una rica historia. Destacan el Parque El Llano Subercaseaux, la Plaza de San Miguel y el Centro Cultural San Miguel.",
    #         "imagen": "Comunas/San Miguel.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 14,
    #         "nombre": "San Ramón",
    #         "descripcion": "San Ramón es una comuna popular y diversa. Lugares de interés incluyen el Cerro Chena, el Parque La Bandera y la Iglesia de San Ramón.",
    #         "imagen": "Comunas/San Ramon.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 15,
    #         "nombre": "San Joaquín",
    #         "descripcion": "San Joaquín es una comuna con un ambiente universitario debido a la presencia de la Universidad de Santiago de Chile. Lugares destacados incluyen el Parque Ohiggins y la Iglesia de San Joaquín.",
    #         "imagen": "Comunas/San Joaquin.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 16,
    #         "nombre": "San José de Maipo",
    #         "descripcion": "San José de Maipo es una comuna rural en las afueras de Santiago, conocida por su belleza natural y actividades al aire libre como senderismo, rafting y observación de estrellas.",
    #         "imagen": "Comunas/San Jose de Maipo.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 17,
    #         "nombre": "Peñalolén",
    #         "descripcion": "Peñalolén es una comuna residencial ubicada en el sector oriente de Santiago. Destacan el Parque Mahuida, el Parque San Luis y la Plaza de la Aviación.",
    #         "imagen": "Comunas/Peñalolen.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 18,
    #         "nombre": "Pedro Aguirre Cerda",
    #         "descripcion": "Pedro Aguirre Cerda es una comuna con una rica historia industrial y cultural. Entre sus atracciones se encuentran el Parque Bicentenario y el Centro Cultural La Granja.",
    #         "imagen": "Comunas/Pedro Aguirre Cerda.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 19,
    #         "nombre": "Pudahuel",
    #         "descripcion": "Pudahuel es una comuna con una mezcla de zonas residenciales e industriales. Destacan el Parque Laguna Sur, el Santuario de la Naturaleza Los Batros y el Museo Aeronáutico y del Espacio.",
    #         "imagen": "Comunas/Pudahuel.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 20,
    #         "nombre": "Lo Prado",
    #         "descripcion": "Lo Prado es una comuna residencial y comercial ubicada en el sector noroeste de Santiago. Destacan la Plaza de Lo Prado, el Parque Ramón Cruz y el Mall Arauco Maipú.",
    #         "imagen": "Comunas/Lo Prado.jpg",
    #         "Clase": "Comuna Segura",
    #     },
    #     {
    #         # "id": 21,
    #         "nombre": "Lo Espejo",
    #         "descripcion": "Lo Espejo es una comuna con una fuerte identidad comunitaria y una gran diversidad cultural. Entre sus atracciones se encuentran la Plaza Lo Espejo y el Centro Cultural El Tranque.",
    #         "imagen": "Comunas/Lo Espejo.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 22,
    #         "nombre": "Lo Barnechea",
    #         "descripcion": "Lo Barnechea es una comuna ubicada en el sector oriente de Santiago, conocida por sus áreas verdes y su calidad de vida. Destacan el Parque Metropolitano de Santiago (Cerro San Cristóbal) y el Parque Bicentenario.",
    #         "imagen": "Comunas/Lo Barnechea.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 23,
    #         "nombre": "La Pintana",
    #         "descripcion": "La Pintana es una comuna ubicada en el sector sur de Santiago, conocida por su diversidad cultural y sus actividades comunitarias. Destacan el Parque El Llano y la Plaza de Armas de La Pintana.",
    #         "imagen": "Comunas/La Pintana.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 24,
    #         "nombre": "La Florida",
    #         "descripcion": "La Florida es una comuna residencial y comercial conocida por sus espacios verdes y su vida cultural. Destacan el Parque Mahuida, el Parque Padre Hurtado y el Mall Plaza Vespucio.",
    #         "imagen": "Comunas/La Florida.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 25,
    #         "nombre": "La Granja",
    #         "descripcion": "La Granja es una comuna ubicada en el sector sur de Santiago, conocida por su diversidad cultural y sus espacios recreativos. Destacan el Parque La Bandera y el Centro Cultural La Granja.",
    #         "imagen": "Comunas/La Granja.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 26,
    #         "nombre": "La Cisterna",
    #         "descripcion": "La Cisterna es una comuna residencial con una rica historia industrial. Destacan el Parque El Llano y la Iglesia de la Cisterna.",
    #         "imagen": "Comunas/La Cisterna.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 27,
    #         "nombre": "Independencia",
    #         "descripcion": "Independencia es una comuna con una mezcla de zonas residenciales e industriales. Destacan el Parque de Los Reyes, el Centro Cultural Matucana 100 y el Barrio Yungay.",
    #         "imagen": "Comunas/Independencia.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 28,
    #         "nombre": "Huechuraba",
    #         "descripcion": "Huechuraba es una comuna residencial y comercial ubicada en el sector norte de Santiago. Destacan el Parque Los Ingleses, el Mall Plaza Norte y el Parque Bicentenario.",
    #         "imagen": "Comunas/Huechuraba.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 29,
    #         "nombre": "El Bosque",
    #         "descripcion": "El Bosque es una comuna con una fuerte identidad comunitaria y una gran diversidad cultural. Entre sus atracciones se encuentran el Parque La Bandera y el Centro Cultural El Bosque.",
    #         "imagen": "Comunas/El Bosque.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 30,
    #         "nombre": "Estación Central",
    #         "descripcion": "Estación Central es una comuna con una importante actividad comercial y de transporte. Destacan la Plaza de la Estación, el Terminal de Buses Alameda y el Museo Ferroviario de Santiago.",
    #         "imagen": "Comunas/Estacion Central.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 31,
    #         "nombre": "Cerrillos",
    #         "descripcion": "Cerrillos es una comuna en desarrollo con una mezcla de zonas residenciales, industriales y comerciales. Destacan el Parque de los Reyes, el Mall Plaza Oeste y el Parque Bicentenario.",
    #         "imagen": "Comunas/Cerrillos.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 32,
    #         "nombre": "Cerro Navia",
    #         "descripcion": "Cerro Navia es una comuna ubicada en el sector norponiente de Santiago. Destacan el Parque San Cristóbal, la Plaza de Cerro Navia y el Teatro Municipal de Cerro Navia.",
    #         "imagen": "Comunas/Cerro Navia.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 33,
    #         "nombre": "Conchalí",
    #         "descripcion": "Conchalí es una comuna con una mezcla de áreas residenciales y comerciales. Destacan el Parque Los Reyes, el Teatro Municipal de Conchalí y el Centro Cultural Conchalí.",
    #         "imagen": "Comunas/Conchali.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 34,
    #         "nombre": "Colina",
    #         "descripcion": "Colina es una comuna ubicada en las afueras de Santiago, conocida por sus paisajes naturales y actividades al aire libre. Destacan el Cerro La Campana, el Parque San Ramón y el Club de Golf Rocas de Santo Domingo.",
    #         "imagen": "Comunas/Colina.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 35,
    #         "nombre": "Buin",
    #         "descripcion": "Buin es una comuna agrícola y vitivinícola ubicada en el valle central de Chile. Destacan los viñedos de la Ruta del Vino y el Parque Safari Buin Zoo.",
    #         "imagen": "Comunas/Buin.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 36,
    #         "nombre": "Calera de Tango",
    #         "descripcion": "Calera de Tango es una comuna ubicada en el valle central de Chile, conocida por su paisaje rural y su tranquilidad. Destacan el Santuario de la Naturaleza Padre Hurtado y la Hacienda Guay-Guay.",
    #         "imagen": "Comunas/Calera de Tango.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 37,
    #         "nombre": "El Monte",
    #         "descripcion": "El Monte es una comuna ubicada en la Provincia de Talagante, en el valle central de Chile. Destacan la Iglesia de El Monte y la Plaza de Armas.",
    #         "imagen": "Comunas/El Monte.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 38,
    #         "nombre": "Isla de Maipo",
    #         "descripcion": "Isla de Maipo es una comuna ubicada en el valle central de Chile, conocida por sus viñedos y actividades relacionadas con el vino. Destacan las viñas de la Ruta del Vino y la Fiesta de la Vendimia.",
    #         "imagen": "Comunas/Isla de Maipo.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 39,
    #         "nombre": "Lampa",
    #         "descripcion": "Lampa es una comuna ubicada en la Provincia de Chacabuco, en el valle central de Chile. Destacan la Iglesia de Lampa y el Parque Padre Hurtado.",
    #         "imagen": "Comunas/Lampa.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 40,
    #         "nombre": "Melipilla",
    #         "descripcion": "Melipilla es una comuna ubicada en la Provincia de Melipilla, en el valle central de Chile. Destacan la Plaza de Armas, el Museo Histórico y el Parque Santa Teresa.",
    #         "imagen": "Comunas/Melipilla.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 41,
    #         "nombre": "Padre Hurtado",
    #         "descripcion": "Padre Hurtado, anteriormente conocida como La Reina, es una comuna ubicada en la Provincia de Talagante, en el valle central de Chile. Destacan el Parque Padre Hurtado y la Iglesia de Padre Hurtado.",
    #         "imagen": "Comunas/Padre Hurtado.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 42,
    #         "nombre": "Paine",
    #         "descripcion": "Paine es una comuna ubicada en la Provincia de Maipo, en el valle central de Chile. Destacan el Parque Nacional Paine, la Reserva Nacional Río Clarillo y la Feria de Paine.",
    #         "imagen": "Comunas/Paine.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 43,
    #         "nombre": "Peñaflor",
    #         "descripcion": "Peñaflor es una comuna ubicada en la Provincia de Talagante, en el valle central de Chile. Destacan la Iglesia de Peñaflor, la Plaza de Armas y la Feria de Peñaflor.",
    #         "imagen": "Comunas/Peñaflor.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 44,
    #         "nombre": "Pirque",
    #         "descripcion": "Pirque es una comuna ubicada en la Provincia Cordillera, en el valle central de Chile. Destacan el Santuario de la Naturaleza El Arrayán, las viñas de Concha y Toro y el Parque Municipal Puente Ñilhue.",
    #         "imagen": "Comunas/Pirque.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 45,
    #         "nombre": "Quilicura",
    #         "descripcion": "Quilicura es una comuna ubicada en el sector norte de Santiago, conocida por su actividad industrial y comercial. Destacan el Parque Municipal Renato Poblete, el Mall Arauco Quilicura y la Feria de Quilicura.",
    #         "imagen": "Comunas/Quilicura.jpg",
    #         "Clase": "Comuna Segura"
    #     }, 
    #     {
    #         # "id": 46,
    #         "nombre": "Macul",
    #         "descripcion": "Macul es una comuna ubicada en el sector oriente de Santiago, conocida por su ambiente residencial y sus espacios verdes. Destacan el Parque San Eugenio, el Estadio Monumental y el Campus San Joaquín de la Pontificia Universidad Católica de Chile.",
    #         "imagen": "Comunas/Macul.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 47,
    #         "nombre": "Talagante",
    #         "descripcion": "Talagante es una comuna ubicada en la Provincia de Talagante, en el valle central de Chile. Destacan la Plaza de Armas, la Iglesia de Talagante y el Museo Histórico de Talagante.",
    #         "imagen": "Comunas/Talagante.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 48,
    #         "nombre": "Tiltil",
    #         "descripcion": "Tiltil es una comuna ubicada en la Provincia de Chacabuco, en el valle central de Chile. Destacan el Cerro La Campana, la Plaza de Armas y la Feria de Tiltil.",
    #         "imagen": "Comunas/Tiltil.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 49,
    #         "nombre": "Alhué",
    #         "descripcion": "Alhué es una comuna ubicada en la Provincia de Melipilla, en el valle central de Chile. Destacan el Embalse La Laguna y la Cascada de los Ángeles.",
    #         "imagen": "Comunas/Alhue.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 50,
    #         "nombre": "Curacaví",
    #         "descripcion": "Curacaví es una comuna ubicada en la Provincia de Melipilla, en el valle central de Chile. Destacan el Río Curacaví, el Cerro El Roble y la Feria de Curacaví.",
    #         "imagen": "Comunas/Curacavi.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 51,
    #         "nombre": "San Pedro",
    #         "descripcion": "San Pedro es una comuna ubicada en la Provincia de Melipilla, en el valle central de Chile. Destacan la Iglesia de San Pedro y la Plaza de Armas.",
    #         "imagen": "Comunas/San Pedro.jpg",
    #         "Clase": "Comuna Segura"
    #     },
    #     {
    #         # "id": 52,
    #         "nombre": "María Pinto",
    #         "descripcion": "María Pinto es una comuna ubicada en la Provincia de Melipilla, en el valle central de Chile. Conocida por su belleza natural y su ambiente rural, ofrece actividades como la visita a viñedos y la observación de aves. Destacan el Cerro El Roble, la Plaza de Armas y la Viña Cousiño Macul.",
    #         "imagen": "Comunas/Maria Pinto.jpg",
    #         "Clase": "Comuna Segura"
    #     }

    # ]

    # print('Crear comunas')
    # for comuna in comunas:
    #     Comuna.objects.create(**comuna)
    print('Comunas creadas correctamente')
