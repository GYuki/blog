from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views import View

class CustomLoginView(View):
    def __init__(self):
        self.username = self.password = ''


    def get(self, request):
        return render(request, 'signup/login.html')

    def post(self, request):
        logout(request)
        self.username = request.POST['username']
        self.password = request.POST['password']

        user = authenticate(username=self.username, password=self.password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('blogsite:feed'))
        return render(request, 'signup/login.html')

class CustomLogoutView(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('signupapp:login'))
    def post(self, request):
        pass
