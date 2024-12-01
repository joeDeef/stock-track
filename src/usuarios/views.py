from django.shortcuts import render, redirect
from django.contrib import messages
from usuarios.models import UsuarioPersonalizado
from django.contrib.auth import authenticate, login
from portafolio.models import Portafolio
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

def get_login(request):
    return render(request, 'login.html')

def get_signup(request):
    return render(request, 'registrar.html')

def authenticate_user(request, email, password):
    return authenticate(request, username=email, password=password)

def create_user(nombres, email, telefono, password):
    usuario = UsuarioPersonalizado(
        nombres=nombres,
        username=email,
        email=email,
        telefono=telefono
    )
    usuario.set_password(password)
    usuario.save()
    Portafolio.objects.create(usuario=usuario)
    return usuario

def iniciar_sesion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate_user(request, email, password)

        if user:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('/compras/')
        messages.error(request, 'Correo electrónico o contraseña incorrectos.')
    return redirect('usuarios:login')

def crear_cuenta(request):
    if request.method == 'POST':
        nombre_completo = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        password = request.POST.get('password')

        if not all([nombre_completo, email, password]):
            messages.error(request, 'Los campos obligatorios no deben estar vacíos.')
            return redirect('usuarios:signup')

        if UsuarioPersonalizado.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado.')
            return redirect('usuarios:signup')

        try:
            create_user(nombre_completo, email, telefono, password)
            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect('usuarios:login')
        except Exception as e:
            messages.error(request, f'Error al crear la cuenta: {str(e)}')

    return redirect('usuarios:signup')

@login_required
def perfil(request):
    return render(request, 'perfil.html', {'usuario': request.user})

def update_perfil(request):
    if request.method == 'POST':
        usuario = request.user

        # Datos del formulario
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        contraseña_actual = request.POST.get('contraseña_actual')
        nueva_contraseña = request.POST.get('nueva_contraseña')

        # Validaciones
        if not check_password(contraseña_actual, usuario.password):
            messages.error(request, "La contraseña actual es incorrecta.")
            return redirect('usuarios:perfil')

        if nueva_contraseña and len(nueva_contraseña) < 8:
            messages.error(request, "La nueva contraseña debe tener al menos 8 caracteres.")
            return redirect('usuarios:perfil')

        # Actualizamos los datos del usuario
        usuario.nombres = nombre
        usuario.email = email
        usuario.telefono = telefono

        if nueva_contraseña:
            usuario.set_password(nueva_contraseña)  # Actualizamos la contraseña

        usuario.save()  # Guardamos los cambios en la base de datos

        # Volvemos a autenticar al usuario
        if nueva_contraseña:
            usuario = authenticate_user(request, usuario.username, nueva_contraseña)
            if usuario:
                login(request, usuario)  # Mantenemos la sesión activa

        messages.success(request, "Tu perfil ha sido actualizado correctamente.")
    return redirect('usuarios:perfil')