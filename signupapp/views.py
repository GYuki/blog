from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.template import RequestContext
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.core.urlresolvers import reverse
from models import UserProfile


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
                return redirect(reverse('signupapp:view_profile'))

    return render(request, 'signup/login.html', context_instance=RequestContext(request))

def custom_logout(request):
    logout(request)
    return redirect(reverse('signupapp:login'))
