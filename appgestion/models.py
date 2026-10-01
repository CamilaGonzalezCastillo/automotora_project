from django.db import models

class UsuarioSistema(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.rut})"

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.rut})"

class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.anio})"

class VehiculoVendido(models.Model):
    id_venta = models.AutoField(primary_key=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha_venta = models.DateField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    comprador = models.CharField(max_length=150)

    def precio_formateado(self):
        try:
            val = str(self.precio_venta).split('.')[0].replace('.', '')
            return f"{int(val):,}".replace(",", ".")
        except:
            return self.precio_venta

    def __str__(self):
        return f"Venta #{self.id_venta} - {self.vehiculo.marca} {self.vehiculo.modelo}"