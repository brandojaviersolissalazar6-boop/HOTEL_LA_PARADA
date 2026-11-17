from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from .models import *
from .forms import *

@login_required
def dashboard(request):
    context={'clientes':Cliente.objects.count(),'habitaciones':Habitacion.objects.count(),'disponibles':Habitacion.objects.filter(estado='Disponible').count(),'reservaciones':Reservacion.objects.exclude(estado='Cancelada').count(),'ingresos':Pago.objects.aggregate(s=Sum('monto'))['s'] or 0,'pendientes':Incidencia.objects.exclude(estado='Resuelta').count(),'ultimas':Reservacion.objects.select_related('cliente','habitacion').order_by('-creado')[:6],'ocupacion':Habitacion.objects.filter(estado='Ocupada').count()}
    return render(request,'gestion/dashboard.html',context)

@login_required
def listado(request, tipo):
    configs={
      'clientes':('Huéspedes',Cliente,ClienteForm,'nombre'), 'habitaciones':('Habitaciones',Habitacion,HabitacionForm,'numero'),
      'reservaciones':('Reservaciones',Reservacion,ReservacionForm,'cliente__nombre'), 'pagos':('Pagos y facturación',Pago,PagoForm,'reservacion__cliente__nombre'),
      'servicios':('Servicios del hotel',Servicio,ServicioForm,'nombre'), 'incidencias':('Mantenimiento',Incidencia,IncidenciaForm,'titulo'),
      'limpieza':('Limpieza',TareaLimpieza,TareaLimpiezaForm,'habitacion__numero'), 'personal':('Personal',Empleado,EmpleadoForm,'nombre')}
    if tipo not in configs: return redirect('dashboard')
    title,model,formclass,searchfield=configs[tipo]; qs=model.objects.all().order_by('-pk')
    q=request.GET.get('q','')
    if q: qs=qs.filter(**{searchfield+'__icontains':q})
    if request.method=='POST':
        form=formclass(request.POST)
        if form.is_valid(): form.save(); messages.success(request,'El registro se guardó correctamente.'); return redirect('listado',tipo=tipo)
    else: form=formclass()
    return render(request,'gestion/listado.html',{'titulo':title,'tipo':tipo,'registros':qs,'form':form,'q':q,'total':qs.count()})

@login_required
def base_datos(request):
    tablas=[('Huéspedes','gestion_cliente',Cliente.objects.all(),['nombre','telefono','correo','documento']),('Habitaciones','gestion_habitacion',Habitacion.objects.all(),['numero','tipo','capacidad','precio_noche','estado']),('Reservaciones','gestion_reservacion',Reservacion.objects.select_related('cliente','habitacion'),['cliente','habitacion','entrada','salida','estado']),('Pagos','gestion_pago',Pago.objects.select_related('reservacion'),['reservacion','monto','metodo','fecha']),('Servicios','gestion_servicio',Servicio.objects.all(),['nombre','categoria','precio','activo']),('Incidencias','gestion_incidencia',Incidencia.objects.select_related('habitacion'),['habitacion','titulo','prioridad','estado']),('Limpieza','gestion_tarealimpieza',TareaLimpieza.objects.select_related('habitacion'),['habitacion','responsable','estado','fecha']),('Personal','gestion_empleado',Empleado.objects.all(),['nombre','puesto','telefono','activo'])]
    return render(request,'gestion/base_datos.html',{'tablas':tablas,'activa':request.GET.get('tabla','Huéspedes')})

@login_required
def reportes(request):
    total=Pago.objects.aggregate(s=Sum('monto'))['s'] or 0
    return render(request,'gestion/reportes.html',{'ingresos':total,'reservas':Reservacion.objects.count(),'habitaciones':Habitacion.objects.count(),'ocupadas':Habitacion.objects.filter(estado='Ocupada').count(),'servicios':ConsumoServicio.objects.count(),'pagos':Pago.objects.select_related('reservacion__cliente').order_by('-fecha')[:10]})
