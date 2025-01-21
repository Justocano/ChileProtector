from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from core.templatetags.custom_filters import formatear_dinero
from django.db import models
from django.db.models import Min
from django.db import connection
from django.conf import settings

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nombre categoría')
    
    class Meta:
        db_table = 'Categoria'
        verbose_name = "Categoría de producto"
        verbose_name_plural = "Categorías de productos"
        ordering = ['nombre']
    
    def __str__(self):
        return f'{self.nombre}'
    
    def acciones(self):
        return {
            'accion_eliminar': 'eliminar la Categoría',
            'accion_actualizar': 'actualizar la Categoría'
        }

class Comuna(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    nombre = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nombre Comuna')
    descripcion = models.CharField(max_length=400, blank=False, null=False, verbose_name='Descripción')
    imagen = models.ImageField(upload_to='productos/', blank=False, null=False, verbose_name='Imagen')
    Clase = models.CharField(max_length=100, blank=False, null=False, verbose_name='Clase')
    class Meta:
        db_table = 'Comuna'
        verbose_name = "Comuna"
        verbose_name_plural = "Comunas"
        ordering = ['id', 'nombre']

    def __str__(self):
        return f'{self.nombre} (ID {self.id})'
    
    def acciones():
        return {
            'accion_eliminar': 'eliminar el Producto',
            'accion_actualizar': 'actualizar el Producto'
        }


class Servicio(models.Model):
    # categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, verbose_name='Categoría')
    nombre = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nombre del servicio')
    descripcion = models.CharField(max_length=400, blank=False, null=False, verbose_name='Descripción')
    precio = models.IntegerField(blank=False, null=False, verbose_name='Precio')
    
    imagen = models.ImageField(upload_to='productos/', blank=False, null=False, verbose_name='Imagen')
    
    class Meta:
        db_table = 'Servicio'
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = [ 'nombre'] 

    def __str__(self):
        return f'{self.nombre} '
    
    def acciones():
        return {
            'accion_eliminar': 'eliminar el Servicios',
            'accion_actualizar': 'actualizar el Servicios'
        }

class Perfil(models.Model):
    USUARIO_CHOICES = [
        ('Cliente', 'Cliente'),
        ('Administrador', 'Administrador'),
        ('Superusuario', 'Superusuario'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(
        choices=USUARIO_CHOICES,
        max_length=50,
        blank=False,
        null=False,
        verbose_name='Tipo de usuario'
    )
    rut = models.CharField(max_length=15, blank=False, null=False, verbose_name='RUT')
    direccion = models.CharField(max_length=400, blank=False, null=False, verbose_name='Dirección')
    subscrito = models.BooleanField(blank=False, null=False, verbose_name='Subscrito')
    imagen = models.ImageField(upload_to='perfiles/', blank=False, null=False, verbose_name='Imagen')
    
    class Meta:
        db_table = 'Perfil'
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuarios"
        ordering = ['tipo_usuario']

    def __str__(self):
        subscrito = ''
        if self.tipo_usuario == 'Cliente':
            subscrito = ' subscrito' if self.subscrito else ' no subscrito'
        return f'{self.usuario.first_name} {self.usuario.last_name} (ID {self.id} - {self.tipo_usuario}{subscrito})'
    
    def acciones():
        return {
            'accion_eliminar': 'eliminar el Perfil',
            'accion_actualizar': 'actualizar el Perfil'
        }

class Pago(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=[
        ('pendiente', 'Pendiente'),
        ('completo', 'Completo'),
        ('fallido', 'Fallido'),
    ], default='pendiente')
    metodo_pago = models.CharField(max_length=50, blank=True, null=True)
    identificador_transaccion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Pago de {self.usuario.username} por {self.monto} - {self.estado}' 