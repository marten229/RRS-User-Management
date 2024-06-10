from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_protect
from .forms import RegisterForm, CustomUserCreationForm, CustomUserChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
@user_passes_test(lambda u: u.role == 'administrator')
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'create_user.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.role == 'administrator')
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'update_user.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.role == 'administrator')
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'confirm_delete.html', {'user': user})

@login_required
@user_passes_test(lambda u: u.role == 'administrator')
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})