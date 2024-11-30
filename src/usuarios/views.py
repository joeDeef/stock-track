from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User  # Para crear usuarios
from django.contrib import messages  # Para mostrar mensajes de éxito o error
from usuarios.models import UsuarioPersonalizado
from django.contrib.auth import authenticate, login
from portafolio.models import Portafolio

def get_login(request):
    return render(request, 'login.html')

def get_signup(request):
    return render(request, 'registrar.html')

def iniciar_sesion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Autenticar al usuario por email
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Si la autenticación es exitosa, inicia sesión
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('/compras/')
        else:
            # Si la autenticación falla
            messages.error(request, 'Correo electrónico o contraseña incorrectos.')
            return redirect('usuarios:login')

    return redirect('usuarios:login')

def crear_cuenta(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre_completo = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        password = request.POST.get('password')

        # Validar que los campos obligatorios no estén vacíos
        if not nombre_completo or not email or not password:
            messages.error(request, 'Los campos Nombre Completo, Email y Contraseña son obligatorios.')
            return redirect('usuarios:signup')

        # Verificar si el email ya está registrado
        if UsuarioPersonalizado.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado.')
            return redirect('usuarios:signup')

        try:
            # Crear una nueva instancia de UsuarioPersonalizado
            usuario = UsuarioPersonalizado(
                nombres=nombre_completo,
                username=email,  # Usa el email como username si lo prefieres
                email=email,
                telefono=telefono
            )
            
            # Cifrar la contraseña antes de guardarla
            usuario.set_password(password)
            
            # Guardar el usuario en la base de datos
            usuario.save()
            
            # Crear el portafolio
            portafolio = Portafolio(usuario=usuario)
            portafolio.save()

            # Mensaje de éxito
            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect('usuarios:login')

        except Exception as e:
            # Si ocurre un error al guardar, muestra un mensaje de error
            messages.error(request, f'Error al crear la cuenta: {str(e)}')
            return redirect('usuarios:signup')

    return redirect('usuarios:signup')
