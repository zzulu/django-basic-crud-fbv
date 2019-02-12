from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


def login(request):
    if request.user.is_authenticated:
        return redirect('posts:list')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'posts:list')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {
        'form': form,
    })


def logout(request):
    auth_logout(request)
    return redirect('posts:list')


def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('posts:list')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {
        'form': form,
    })
