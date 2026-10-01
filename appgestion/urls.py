from django.urls import path
from appgestion.views import (
    login_view, logout_view, menu_principal,
    agregar_cliente_vehiculo, agregar_vehiculo_vendido,
    listar_clientes_vehiculos, buscar_cliente,
    listar_vehiculos_vendidos, eliminar_vehiculo,
    crear_usuario_inicial
)

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('menu/', menu_principal, name='menu_principal'),
    path('agregar_cliente_vehiculo/', agregar_cliente_vehiculo, name='agregar_cliente_vehiculo'),
    path('agregar_vehiculo_vendido/', agregar_vehiculo_vendido, name='agregar_vehiculo_vendido'),
    path('listar_clientes_vehiculos/', listar_clientes_vehiculos, name='listar_clientes_vehiculos'),
    path('buscar_cliente/', buscar_cliente, name='buscar_cliente'),
    path('listar_vehiculos_vendidos/', listar_vehiculos_vendidos, name='listar_vehiculos_vendidos'),
    path('eliminar_vehiculo/', eliminar_vehiculo, name='eliminar_vehiculo'),
    path('crear_usuario_inicial/', crear_usuario_inicial, name='crear_usuario_inicial'),
]