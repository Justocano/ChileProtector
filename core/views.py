# Create your views here.
from django.shortcuts import  render, redirect
from datetime import date
from django.contrib.auth.models import User
from .poblar import poblar_bd
from .models import Perfil,Servicio,Comuna,Pago
from .forms import RegistroClienteForm, IngresarForm,ServicioForm,UsuarioForm,PagoForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .integracion import obtener_comunas , obtener_comuna, buscar_comunas_por_nombre, obtener_regiones, obtener_region
from .tools import eliminar_registro #, verificar_eliminar_registro
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .noticias import obtener_noticias 
# from core.templatetags.custom_filters import formatear_dinero, formatear_numero
# from .models import Mascota

# Create your views here.

def inicio(request):
    comunas = obtener_comunas()
    regiones = obtener_regiones()
    error_message = None if comunas else 'No se pudo obtener los datos de la API'
    error_message1 = None if regiones else 'No se pudo obtener los datos de la API en regiones'
    comunas_filtradas = comunas
    
    # Filtrado por región
    region_id = request.GET.get('region_id')
    if region_id:
        comunas_filtradas = [comuna for comuna in comunas if comuna['regionId'] == int(region_id)]
        if not comunas_filtradas:
            error_message = f"No se encontraron comunas para la región seleccionada."

    # Búsqueda por nombre
    if request.method == 'POST':
        nombre_comuna = request.POST.get('q', '').strip()
        comunas_filtradas = buscar_comunas_por_nombre(nombre_comuna)
        
        if not comunas_filtradas:
            error_message = f"No se encontró ninguna comuna con el nombre: {nombre_comuna.capitalize()}"
    # Llamar a la función que obtiene las noticias


    # Llamar a la función que obtiene las noticias
    

    # Pasar los artículos al template
    context = {
        'comunas': comunas_filtradas,
        'regiones': regiones,
        'error_message': error_message,
        'error_message1': error_message1
    }

    return render(request, "core/inicio.html", context)


def ficha(request, comuna_id):
    comuna = obtener_comuna(comuna_id)
    regiones = obtener_regiones()
    articles = obtener_noticias(comuna_id)
    context = {
        'articles': articles,
        'comuna': comuna,
        'regiones': regiones,
        'error_message': None if comuna else 'No se pudo obtener los datos de la comuna',
        'error_message1': None if regiones else 'No se pudo obtener los datos de las regiones'
    }

    return render(request, 'core/ficha.html', context)

def reserva(request):
    return render(request,'core/Reserva.html')

def salir(request):
    logout(request)
    return redirect(inicio)

def obtener_info_producto(comuna_id):

    comunas = Comuna.objects.get(id=comuna_id)
    
    return {
        'id':comunas.id,
        'nombre': comunas.nombre,
        'descripcion': comunas.descripcion,
        'imagen': comunas.imagen,
        'clase': comunas.Clase,
    }


def _servicios(request, accion, id):
    comunas = obtener_comunas()
    error_message = None if comunas else 'No se pudo obtener los datos de la API'
    
    if request.method == 'POST':
        nombre_comuna = request.POST.get('q', '').strip()
        comuna = buscar_comuna_por_nombre(nombre_comuna)
        
        if comuna:
            return redirect(reverse('ficha', args=[comuna['id']]))
        else:
            error_message = f"No se encontró ninguna comuna con el nombre: {nombre_comuna.capitalize()}"
    
    context = {
        'comunas': comunas,
        'error_message': error_message
    }
    return render(request, 'core/servicios.html', context)

def poblar(request):
    poblar_bd()
    return redirect(inicio)

def registroUser(request):
    form = RegistroClienteForm()
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            rut = form.cleaned_data['rut']
            direccion = form.cleaned_data['direccion']
            subscrito = form.cleaned_data['subscrito']
            Perfil.objects.create(
                usuario=user, 
                tipo_usuario='Cliente', 
                rut=rut, 
                direccion=direccion, 
                subscrito=subscrito,
                imagen=request.FILES['imagen'])
            return redirect(usuarios, 'crear', '0')
            
    return render(request, "core/registroUser.html", {'form': form})


def registro(request):
    form = RegistroClienteForm()
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            rut = form.cleaned_data['rut']
            direccion = form.cleaned_data['direccion']
            subscrito = form.cleaned_data['subscrito']
            Perfil.objects.create(
                usuario=user, 
                tipo_usuario='Cliente', 
                rut=rut, 
                direccion=direccion, 
                subscrito=subscrito,
                imagen=request.FILES['imagen'])
            return redirect(ingresar)
            
    return render(request, "core/registro.html", {'form': form})

@login_required
def misDatos(request):
    usuario = request.user
    perfil, created = Perfil.objects.get_or_create(usuario=usuario)

    if request.method == 'POST':
        form = RegistroClienteForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            user = form.save()
            perfil.rut = form.cleaned_data['rut']
            perfil.direccion = form.cleaned_data['direccion']
            perfil.subscrito = form.cleaned_data['subscrito']
            if 'imagen' in request.FILES:
                perfil.imagen = request.FILES['imagen']
            perfil.save()
            return redirect('misDatos')
    else:
        form = RegistroClienteForm(instance=usuario, initial={
            'rut': perfil.rut,
            'direccion': perfil.direccion,
            'subscrito': perfil.subscrito,
            'imagen': perfil.imagen,
        })

    return render(request, "core/misDatos.html", {'form': form, 'perfil': perfil})

def salir(request):
    logout(request)
    return redirect(inicio)


def ingresar(request):

    if request.method == "POST":
        form = IngresarForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(inicio)
            messages.error(request, 'La cuenta o la password no son correctos')
    
    return render(request, "core/ingresar.html", {
        'form':  IngresarForm(),
        'perfiles': Perfil.objects.all(),
    })


def miscompras(request):
    return render(request, 'core/miscompras.html')



def nosotros(request):
    return render(request, "core/nosotros.html")

def piePagina(request):
    return render(request, "core/piePagina.html")


def usuarios(request,accion,id):
    if request.method == 'GET':

        if accion == 'crear':
            form = UsuarioForm()

        elif accion == 'actualizar':
            form = UsuarioForm(instance=Perfil.objects.get(id=id))

        elif accion == 'eliminar':
            messages.success(request, eliminar_registro(Perfil, id))
            return redirect(usuarios, 'crear', '0')

    if request.method == 'POST':

        if accion == 'crear':
            form = UsuarioForm(request.POST, request.FILES)

        elif accion == 'actualizar':
            form = UsuarioForm(request.POST, request.FILES, instance=Perfil.objects.get(id=id))

        if form.is_valid():
            perfil = form.save()
            form = UsuarioForm(instance=perfil)
            messages.success(request, f'El Perfil "{str(perfil)}" se logró {accion} correctamente')
            return redirect(usuarios, 'actualizar', perfil.id)
        else:
            messages.error(request, f'No se pudo {accion} el Perfil, pues el formulario no pasó las validaciones básicas')
            return redirect(usuarios, 'actualizar', id)

    

    perfil = Perfil.objects.all()

    datos = {
        'form': form,
        'perfiles': perfil
    }
    return render(request, "core/usuarios.html",datos)

def suscripcion(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            nuevo_pago = form.save(commit=False)
            nuevo_pago.usuario = request.user  # Asigna el usuario actual al pago
            nuevo_pago.save()
            messages.success(request, 'Pago creado correctamente.')
            return redirect('pagina_exito')  # Redirige a una página de éxito
        else:
            messages.error(request, 'No se pudo crear el pago. Verifique los datos ingresados.')
    else:
        form = PagoForm()

    return render(request, 'core/suscripcion.html', {'form': form})