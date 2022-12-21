from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import render, redirect

from authentication.forms import RegisterUserForm, AuthorizationUserForm


# Create your views here.

def authorization(request):
    if request.method == 'POST':
        form = AuthorizationUserForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('category')
    else:
        form = AuthorizationUserForm()
    return render(request, 'authentication/password.html', {"form": form})


def password_recovery(request):
    return render(request, 'authentication/password-sbros.html')


def registerUser(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('authorization')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = RegisterUserForm()

    return render(request, 'authentication/register.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('category')
