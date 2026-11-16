# HOTEL LA PARADA — Sistema de administración hotelera

Proyecto académico desarrollado con Python y Django, con base de datos SQLite.

## Módulos incluidos
- Panel principal con indicadores y reservaciones recientes.
- Huéspedes y habitaciones.
- Reservaciones con validación de fechas y prevención de traslapes de habitación.
- Pagos y facturación (registro de anticipos y pagos).
- Catálogo de servicios y consumos adicionales (modelo de datos).
- Mantenimiento mediante incidencias y prioridades.
- Limpieza y seguimiento de tareas.
- Personal y puestos.
- Reportes con resumen de ingresos, reservaciones y ocupación.
- Explorador de base de datos con pestañas, conteos y estructura desplegable de tablas.
- Panel administrativo de Django.

## Instalación en Windows
1. Extrae el ZIP en una carpeta nueva.
2. Abre esa carpeta en Visual Studio Code.
3. Abre Terminal > New Terminal.
4. Ejecuta, una línea a la vez:

```bat
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
py manage.py makemigrations gestion
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

5. Abre http://127.0.0.1:8000/ e inicia sesión con el usuario que creaste.
6. Para administrar directamente todos los registros, visita http://127.0.0.1:8000/admin/.

La base de datos `db.sqlite3` se crea automáticamente al ejecutar `py manage.py migrate`. No se incluye una base de datos precargada para evitar registros ficticios; agrega datos desde los módulos o desde `/admin/`.

## Consideraciones
- La interfaz carga Bootstrap desde CDN, por lo que requiere conexión a internet para ese recurso visual.
- Es una versión académica/local. Antes de publicar en internet deben cambiarse `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` y configurarse HTTPS y validaciones de seguridad adicionales.
