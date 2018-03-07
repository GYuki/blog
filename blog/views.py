from django.shortcuts import redirect

def login_redirect(request):
    if request.user.is_authenticated():
        return redirect('blogsite:feed')
    return redirect('signupapp:login')
