from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User, Group

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Verificar se é admin
            if user.is_staff:
                # Adicionar ao grupo de administradores se ainda não estiver
                admin_group = Group.objects.get(name='Administradores')
                if not user.groups.filter(name='Administradores').exists():
                    user.groups.add(admin_group)
            else:
                # Adicionar ao grupo de usuários normais se ainda não estiver
                user_group = Group.objects.get(name='Usuarios')
                if not user.groups.filter(name='Usuarios').exists():
                    user.groups.add(user_group)
            
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('/products/')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
            
    return render(request, 'login.html')

def criar_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_admin = request.POST.get('is_admin') == 'on'  # checkbox no form
        
        try:
            if is_admin:
                # Criar usuário administrador
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                messages.success(request, 'Administrador criado com sucesso!')
            else:
                # Criar usuário normal
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                messages.success(request, 'Usuário criado com sucesso!')
                
            return redirect('login')  # redireciona para a página de login
            
        except Exception as e:
            messages.error(request, f'Erro ao criar usuário: {str(e)}')
    
    return render(request, 'register.html')