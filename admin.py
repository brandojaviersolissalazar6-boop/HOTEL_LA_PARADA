from django.contrib import admin
from .models import Cliente,Habitacion,Reservacion,Pago,Servicio,ConsumoServicio,Incidencia,TareaLimpieza,Empleado
admin.site.site_header = 'HOTEL LA PARADA | Administración'
admin.site.site_title = 'Hotel La Parada'
admin.site.index_title = 'Centro de control'
for model in [Cliente,Habitacion,Reservacion,Pago,Servicio,ConsumoServicio,Incidencia,TareaLimpieza,Empleado]: admin.site.register(model)
