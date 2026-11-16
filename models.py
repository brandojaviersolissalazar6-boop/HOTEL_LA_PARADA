from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    telefono = models.CharField(max_length=25, blank=True)
    correo = models.EmailField(blank=True)
    documento = models.CharField(max_length=40, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.nombre

class Habitacion(models.Model):
    TIPOS = [('Sencilla','Sencilla'),('Doble','Doble'),('Suite','Suite'),('Familiar','Familiar')]
    ESTADOS = [('Disponible','Disponible'),('Ocupada','Ocupada'),('Limpieza','En limpieza'),('Mantenimiento','Mantenimiento')]
    numero = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    capacidad = models.PositiveSmallIntegerField(default=2)
    precio_noche = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Disponible')
    piso = models.PositiveSmallIntegerField(default=1)
    descripcion = models.TextField(blank=True)
    def __str__(self): return f'Habitación {self.numero}'

class Reservacion(models.Model):
    ESTADOS = [('Confirmada','Confirmada'),('Hospedado','Hospedado'),('Finalizada','Finalizada'),('Cancelada','Cancelada')]
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='reservaciones')
    habitacion = models.ForeignKey(Habitacion, on_delete=models.PROTECT, related_name='reservaciones')
    entrada = models.DateField()
    salida = models.DateField()
    personas = models.PositiveSmallIntegerField(default=1)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Confirmada')
    notas = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    @property
    def noches(self): return max((self.salida-self.entrada).days, 0)
    @property
    def total(self): return self.noches * self.habitacion.precio_noche
    def __str__(self): return f'Reservación #{self.pk} - {self.cliente}'

class Pago(models.Model):
    METODOS = [('Efectivo','Efectivo'),('Tarjeta','Tarjeta'),('Transferencia','Transferencia')]
    reservacion = models.ForeignKey(Reservacion, on_delete=models.CASCADE, related_name='pagos')
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    metodo = models.CharField(max_length=20, choices=METODOS)
    referencia = models.CharField(max_length=80, blank=True)
    fecha = models.DateTimeField(default=timezone.now)
    observaciones = models.CharField(max_length=200, blank=True)
    def __str__(self): return f'Pago {self.pk} - ${self.monto}'

class Servicio(models.Model):
    CATEGORIAS = [('Lavandería','Lavandería'),('Transporte','Transporte'),('Alimentos','Alimentos'),('Otro','Otro')]
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    precio = models.DecimalField(max_digits=9, decimal_places=2)
    activo = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True)
    def __str__(self): return self.nombre

class ConsumoServicio(models.Model):
    reservacion = models.ForeignKey(Reservacion, on_delete=models.CASCADE, related_name='consumos')
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)
    cantidad = models.PositiveSmallIntegerField(default=1)
    fecha = models.DateTimeField(default=timezone.now)
    @property
    def subtotal(self): return self.cantidad * self.servicio.precio

class Incidencia(models.Model):
    ESTADOS = [('Pendiente','Pendiente'),('En proceso','En proceso'),('Resuelta','Resuelta')]
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE, related_name='incidencias')
    titulo = models.CharField(max_length=120)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=15, choices=[('Baja','Baja'),('Media','Media'),('Alta','Alta')], default='Media')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    fecha_reporte = models.DateTimeField(auto_now_add=True)

class TareaLimpieza(models.Model):
    ESTADOS = [('Pendiente','Pendiente'),('En proceso','En proceso'),('Terminada','Terminada')]
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE, related_name='tareas_limpieza')
    responsable = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    fecha = models.DateField(default=timezone.localdate)
    observaciones = models.TextField(blank=True)

class Empleado(models.Model):
    PUESTOS = [('Recepción','Recepción'),('Limpieza','Limpieza'),('Mantenimiento','Mantenimiento'),('Administración','Administración')]
    nombre = models.CharField(max_length=120)
    puesto = models.CharField(max_length=30, choices=PUESTOS)
    telefono = models.CharField(max_length=25, blank=True)
    correo = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_ingreso = models.DateField(default=timezone.localdate)
    def __str__(self): return self.nombre
