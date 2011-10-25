from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.

from forms import SignupForm

def signup(request):
    # can't sign up if they're already signed in!
    #if request.user.is_authenticated():
    #   return HttpResponseRedirect("/accounts/home")
    
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/accounts/login")
    else:
        form = SignupForm()
    return render_to_response('useraccounts/signup.html',
                              {'form':form,
                    })

@login_required
def view_home(request):
    user_profile = request.user.get_profile
    
    return render_to_response('useraccounts/home.html',{'profile': user_profile})
    
def login(request):
    return render_to_response('useraccounts/login.html', {})