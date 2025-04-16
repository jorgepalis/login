from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserBasicInfoForm, PersonalInfoForm, AddressInfoForm, AdditionalInfoForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required

def home(request):
    """Vista para la página de inicio"""
    return render(request, 'account/home.html')

def user_login(request):
    """Vista para el inicio de sesión"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Verificar si el usuario tiene un perfil completo
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.profile_complete:
                    messages.success(request, '¡Bienvenido de nuevo!')
                    return redirect('account:profile')  # Redirigir al perfil en lugar de home
                else:
                    # Si el registro no está completo, continuar desde el paso correspondiente
                    return redirect(f'account:registro_paso{profile.registration_step}')
            except UserProfile.DoesNotExist:
                messages.success(request, '¡Bienvenido de nuevo!')
                return redirect('account:home')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')
    
    return render(request, 'account/login.html')

def registro_paso1(request):
    """Vista para el primer paso del registro - información básica"""
    # Si está retomando el registro
    usuario_id = request.session.get('registro_usuario_id')
    if (usuario_id):
        try:
            user = User.objects.get(pk=usuario_id)
            profile = UserProfile.objects.get(user=user)
            
            # Si el usuario ya pasó el paso 1, redirigir al paso 2 siempre
            # (esto evita volver al paso 1 una vez avanzado)
            if (profile.registration_step >= 2):
                messages.info(request, "No es posible volver al primer paso del registro.")
                return redirect('account:registro_paso2')
                
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            # Si hay algún error, limpiar la sesión y comenzar de nuevo
            if ('registro_usuario_id' in request.session):
                del request.session['registro_usuario_id']
    
    if (request.method == 'POST'):
        form = UserBasicInfoForm(request.POST)
        if (form.is_valid()):
            # Guardamos el usuario pero no lo autenticamos aún
            user = form.save()
            # Creamos el perfil asociado
            profile = UserProfile.objects.create(
                user=user, 
                registration_step=2
            )
            # Guardamos el ID del usuario en la sesión
            request.session['registro_usuario_id'] = user.id
            messages.success(request, "¡Información básica guardada! Continuemos con el siguiente paso.")
            return redirect('account:registro_paso2')
    else:
        form = UserBasicInfoForm()
    
    return render(request, 'account/paso1.html', {'form': form})

def registro_paso2(request):
    """Vista para el segundo paso del registro - información personal"""
    # Verificar que exista el usuario en sesión
    usuario_id = request.session.get('registro_usuario_id')
    if (not usuario_id):
        messages.warning(request, "Por favor comienza el proceso de registro")
        return redirect('account:registro_paso1')
    
    try:
        user = User.objects.get(pk=usuario_id)
        profile = UserProfile.objects.get(user=user)
        
        # Solo verifica que no intente saltar pasos
        if (profile.registration_step < 2):
            return redirect(f'account:registro_paso{profile.registration_step}')
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        messages.error(request, "Ha ocurrido un error en el registro")
        return redirect('account:registro_paso1')
    
    if (request.method == 'POST'):
        form = PersonalInfoForm(request.POST, instance=profile)
        if (form.is_valid()):
            profile = form.save(commit=False)
            profile.registration_step = 3
            profile.save()
            messages.success(request, "¡Información personal guardada! Continuemos con el siguiente paso.")
            return redirect('account:registro_paso3')
    else:
        form = PersonalInfoForm(instance=profile)
    
    return render(request, 'account/paso2.html', {'form': form})

def registro_paso3(request):
    """Vista para el tercer paso del registro - información de dirección"""
    # Verificar que exista el usuario en sesión
    usuario_id = request.session.get('registro_usuario_id')
    if (not usuario_id):
        messages.warning(request, "Por favor comienza el proceso de registro")
        return redirect('account:registro_paso1')
    
    try:
        user = User.objects.get(pk=usuario_id)
        profile = UserProfile.objects.get(user=user)
        
        if (profile.registration_step < 3):
            return redirect(f'account:registro_paso{profile.registration_step}')
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        messages.error(request, "Ha ocurrido un error en el registro")
        return redirect('account:registro_paso1')
    
    if (request.method == 'POST'):
        form = AddressInfoForm(request.POST, instance=profile)
        if (form.is_valid()):
            profile = form.save(commit=False)
            profile.registration_step = 4
            profile.save()
            messages.success(request, "¡Dirección guardada! Continuemos con el último paso.")
            return redirect('account:registro_paso4')
    else:
        form = AddressInfoForm(instance=profile)
    
    return render(request, 'account/paso3.html', {'form': form})

def registro_paso4(request):
    """Vista para el cuarto paso del registro - información adicional"""
    # Verificar que exista el usuario en sesión
    usuario_id = request.session.get('registro_usuario_id')
    if (not usuario_id):
        messages.warning(request, "Por favor comienza el proceso de registro")
        return redirect('account:registro_paso1')
    
    try:
        user = User.objects.get(pk=usuario_id)
        profile = UserProfile.objects.get(user=user)
        
        if (profile.registration_step < 4):
            return redirect(f'account:registro_paso{profile.registration_step}')
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        messages.error(request, "Ha ocurrido un error en el registro")
        return redirect('account:registro_paso1')
    
    if (request.method == 'POST'):
        form = AdditionalInfoForm(request.POST, instance=profile)
        if (form.is_valid()):
            profile = form.save(commit=False)
            profile.profile_complete = True
            profile.save()
            
            # Ahora sí autenticamos al usuario
            login(request, user)
            
            # Limpiamos la sesión
            if ('registro_usuario_id' in request.session):
                del request.session['registro_usuario_id']
                
            messages.success(request, "¡Registro completado exitosamente!")
            return redirect('account:registro_completado')
    else:
        form = AdditionalInfoForm(instance=profile)
    
    return render(request, 'account/paso4.html', {'form': form})

def registro_completado(request):
    """Vista de confirmación de registro completo"""
    return render(request, 'account/completado.html')

@login_required
def user_profile(request):
    """Vista para mostrar el perfil del usuario"""
    try:
        profile = UserProfile.objects.get(user=request.user)
        return render(request, 'account/profile.html', {'profile': profile})
    except UserProfile.DoesNotExist:
        messages.error(request, "No se encontró un perfil para este usuario.")
        return redirect('account:home')

def user_logout(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('account:home')
