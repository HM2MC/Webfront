from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as authlogout
from django.template import RequestContext
# Create your views here.

from forms import LoginForm

@login_required
def view_home(request):
    user_profile = request.user.get_profile
    
    return direct_to_template(request, 'accounts/home.html',
                              extra_context={
                               'footer_tagline':"Because we're <em>your</em> family&trade;"
                               },
                              )
