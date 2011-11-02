from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as authlogout
# Create your views here.

from forms import LoginForm

@login_required
def view_home(request):
    user_profile = request.user.get_profile
    
    return render_to_response('accounts/home.html',{'profile': user_profile,
                                                    'user':request.user})
'''
def login(request):
    form = LoginForm()
    
    return render_to_response('accounts/login.html', {'form': form})

def logout(request):
    authlogout(request)
    return HttpResponseRedirect("/flat/loggedout.html")
''' 