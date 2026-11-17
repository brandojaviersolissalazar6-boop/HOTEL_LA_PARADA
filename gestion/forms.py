from django import forms
from .models import Cliente,Habitacion,Reservacion,Pago,Servicio,Incidencia,TareaLimpieza,Empleado
class StyledModelForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
class ClienteForm(StyledModelForm):
    class Meta: model=Cliente; fields=['nombre','telefono','correo','documento']
class HabitacionForm(StyledModelForm):
    class Meta: model=Habitacion; fields=['numero','tipo','capacidad','precio_noche','estado','piso','descripcion']
class ReservacionForm(StyledModelForm):
    class Meta: model=Reservacion; fields=['cliente','habitacion','entrada','salida','personas','estado','notas']; widgets={'entrada':forms.DateInput(attrs={'type':'date'}),'salida':forms.DateInput(attrs={'type':'date'})}
    def clean(self):
        data=super().clean(); a=data.get('entrada'); b=data.get('salida'); room=data.get('habitacion')
        if a and b and b<=a: raise forms.ValidationError('La salida debe ser posterior a la entrada.')
        if a and b and room and Reservacion.objects.filter(habitacion=room,entrada__lt=b,salida__gt=a).exclude(pk=self.instance.pk).exclude(estado='Cancelada').exists(): raise forms.ValidationError('La habitación ya tiene una reservación en esas fechas.')
        return data
class PagoForm(StyledModelForm):
    class Meta: model=Pago; fields=['reservacion','monto','metodo','referencia','observaciones']
class ServicioForm(StyledModelForm):
    class Meta: model=Servicio; fields=['nombre','categoria','precio','activo','descripcion']
class IncidenciaForm(StyledModelForm):
    class Meta: model=Incidencia; fields=['habitacion','titulo','descripcion','prioridad','estado']
class TareaLimpiezaForm(StyledModelForm):
    class Meta: model=TareaLimpieza; fields=['habitacion','responsable','estado','fecha','observaciones']
class EmpleadoForm(StyledModelForm):
    class Meta: model=Empleado; fields=['nombre','puesto','telefono','correo','activo','fecha_ingreso']
