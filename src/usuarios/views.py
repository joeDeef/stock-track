from django.shortcuts import render, redirect
from django.contrib.auth.models import User
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
            usuario = authenticate(request, username=usuario.username, password=nueva_contraseña)
            if usuario:
                login(request, usuario)  # Mantenemos la sesión activa

        # Mensaje de éxito y redirección
        messages.success(request, "Tu perfil ha sido actualizado correctamente.")
        return redirect('usuarios:perfil')

    # Si no es una solicitud POST, redirigimos al perfil
    return redirect('usuarios:perfil')