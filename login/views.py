from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['psw']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/api/malumotlar-qoshish/')
        else:
            messages.info(request, "Login yoki Parol Xato")
            return redirect('/')
    return render(request, 'login.html')


def chiqish(request):
    auth.logout(request)
    return redirect('/')