from django.urls import path
from . import views
urlpatterns=[path('',views.dashboard,name='dashboard'),path('modulo/<str:tipo>/',views.listado,name='listado'),path('base-datos/',views.base_datos,name='base_datos'),path('reportes/',views.reportes,name='reportes')]
