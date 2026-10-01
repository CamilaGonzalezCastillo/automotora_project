from django.contrib import admin
from appgestion.models import UsuarioSistema, Cliente, Vehiculo, VehiculoVendido

admin.site.register(UsuarioSistema)
admin.site.register(Cliente)
admin.site.register(Vehiculo)
admin.site.register(VehiculoVendido)