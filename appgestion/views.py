from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from appgestion.models import UsuarioSistema, Cliente, Vehiculo, VehiculoVendido

# Vista de acceso / Login
def login_view(request):
    if request.method == "POST":
        rut_recibido = request.POST.get("txt_rut", "").strip()
        clave_recibida = request.POST.get("txt_clave", "").strip()

        if len(rut_recibido) == 0 or len(clave_recibida) == 0:
            return render(request, "appgestion/login.html", {"error": "Debe ingresar RUT y clave."})

        try:
            usuario = UsuarioSistema.objects.get(rut=rut_recibido)
            if check_password(clave_recibida, usuario.password):
                request.session["usuario_nombre"] = usuario.nombre
                request.session["usuario_apellido"] = usuario.apellidos
                return redirect("menu_principal")
            else:
                return render(request, "appgestion/login.html", {"error": "Clave incorrecta."})
        except UsuarioSistema.DoesNotExist:
            return render(request, "appgestion/login.html", {"error": "El RUT ingresado no está registrado."})

    return render(request, "appgestion/login.html")

def logout_view(request):
    request.session.flush()
    return redirect("login")

# Menú principal tras autenticarse
def menu_principal(request):
    if "usuario_nombre" not in request.session:
        return redirect("login")
    return render(request, "appgestion/menu.html", {
        "nombre": request.session["usuario_nombre"],
        "apellido": request.session["usuario_apellido"]
    })

# 1. Agregar Cliente y Vehículo
def agregar_cliente_vehiculo(request):
    if "usuario_nombre" not in request.session:
        return redirect("login")

    if request.method == "POST":
        rut = request.POST.get("txt_rut", "").strip()
        nombre = request.POST.get("txt_nombre", "").strip()
        apellidos = request.POST.get("txt_apellidos", "").strip()
        marca = request.POST.get("txt_marca", "").strip()
        modelo = request.POST.get("txt_modelo", "").strip()
        anio = request.POST.get("txt_anio", "").strip()

        if len(rut) > 0 and len(nombre) > 0 and len(apellidos) > 0 and len(marca) > 0 and len(modelo) > 0 and len(anio) > 0:
            cliente, _ = Cliente.objects.get_or_create(
                rut=rut,
                defaults={"nombre": nombre, "apellidos": apellidos}
            )
            Vehiculo.objects.create(
                marca=marca,
                modelo=modelo,
                anio=int(anio),
                cliente=cliente
            )
            return HttpResponse('<h2>Cliente y Vehículo guardados con éxito</h2><br><a href="/menu/">Volver al Menú</a>')
        else:
            return HttpResponse('<h2>Error: Todos los campos son obligatorios y no pueden estar en blanco.</h2><br><a href="/menu/">Volver al Menú</a>')

    return render(request, "appgestion/agregar_cliente_vehiculo.html")

# 2. Agregar Vehículo Vendido
def agregar_vehiculo_vendido(request):
    if "usuario_nombre" not in request.session:
        return redirect("login")

    if request.method == "POST":
        id_vehiculo = request.POST.get("opt_vehiculo", "").strip()
        fecha_venta = request.POST.get("txt_fecha", "").strip()
        precio_venta = request.POST.get("txt_precio", "").strip()
        comprador = request.POST.get("txt_comprador", "").strip()

        if len(id_vehiculo) > 0 and len(fecha_venta) > 0 and len(precio_venta) > 0 and len(comprador) > 0:
            vehiculo = Vehiculo.objects.get(id_vehiculo=id_vehiculo)
            VehiculoVendido.objects.create(
                vehiculo=vehiculo,
                fecha_venta=fecha_venta,
                precio_venta=precio_venta,
                comprador=comprador
            )
            return HttpResponse('<h2>Venta registrada exitosamente</h2><br><a href="/menu/">Volver al Menú</a>')
        else:
            return HttpResponse('<h2>Error: No se permiten campos vacíos.</h2><br><a href="/menu/">Volver al Menú</a>')

    vehiculos = Vehiculo.objects.all()
    return render(request, "appgestion/agregar_vehiculo_vendido.html", {"vehiculos": vehiculos})

# 3. Listar Clientes y Vehículos
def listar_clientes_vehiculos(request):
    if "usuario_nombre" not in request.session:
        return redirect("login")
    vehiculos = Vehiculo.objects.select_related("cliente").all()
    return render(request, "appgestion/listar_clientes_vehiculos.html", {"vehiculos": vehiculos})

# 4. Buscar Cliente por RUT
def buscar_cliente(request):
    if "usuario_nombre" not in request.session:
        return redirect("login")

    busqueda_realizada = False
    cliente = None
    vehiculos = []

    if "txt_rut" in request.GET:
        rut = request.GET["txt_rut"].strip()
        if len(rut) > 0:
            busqueda_realizada = True
            cliente = Cliente.objects.filter(rut=rut).first()
            if cliente:
                vehiculos = Vehiculo.objects.filter(cliente=cliente)

    return render(request, "appgestion/buscar_cliente.html", {
        "busqueda_realizada": busqueda_realizada,
        "cliente": cliente,
        "vehiculos": vehiculos
    })

# 5. Listar Vehículos Vendidos
def listar_vehiculos_vendidos(request):
    if "usuario_nombre" not in request.session:
        return redirect("login")
    ventas = VehiculoVendido.objects.select_related("vehiculo", "vehiculo__cliente").all()
    return render(request, "appgestion/listar_vehiculos_vendidos.html", {"ventas": ventas})

# 6. Eliminar Vehículo de un Cliente
def eliminar_vehiculo(request):
    if "usuario_nombre" not in request.session:
        return redirect("login")

    if request.method == "POST":
        id_vehiculo = request.POST.get("txt_id_vehiculo", "").strip()
        if len(id_vehiculo) > 0:
            vehiculo = Vehiculo.objects.filter(id_vehiculo=id_vehiculo)
            if vehiculo:
                v = Vehiculo.objects.get(id_vehiculo=id_vehiculo)
                v.delete()
                return HttpResponse('<h2>Vehículo eliminado exitosamente</h2><br><a href="/menu/">Volver al Menú</a>')
            else:
                return HttpResponse('<h2>Producto No eliminado. No existe vehículo con ese código</h2><br><a href="/menu/">Volver al Menú</a>')
        else:
            return HttpResponse('<h2>Debe seleccionar un vehículo válido</h2><br><a href="/menu/">Volver al Menú</a>')

    vehiculos = Vehiculo.objects.select_related("cliente").all()
    return render(request, "appgestion/eliminar_vehiculo.html", {"vehiculos": vehiculos})

# Vista auxiliar para insertar el usuario base con clave encriptada
def crear_usuario_inicial(request):
    if not UsuarioSistema.objects.filter(rut="12.345.678-9").exists():
        UsuarioSistema.objects.create(
            rut="12.345.678-9",
            nombre="Claudio",
            apellidos="Fuenzalida Medina",
            password=make_password("inacap2026")
        )
        return HttpResponse('<h2>Usuario creado: RUT 12.345.678-9 / Clave: inacap2026</h2><br><a href="/">Ir al Login</a>')
    return HttpResponse('<h2>El usuario ya existe</h2><br><a href="/">Ir al Login</a>')