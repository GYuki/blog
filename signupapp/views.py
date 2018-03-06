from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse

def custom_login(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse("Good")

    return render(request, 'signup/login.html')

def custom_logout(request):
    logout(request)
    return redirect(reverse('signupapp:login'))
