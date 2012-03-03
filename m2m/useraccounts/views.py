from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as authlogout
from django.template import RequestContext
# Create your views here.

from forms import LoginForm

from m2m.polls.models import Poll

@login_required
def view_home(request):
    
    return direct_to_template(request, 'home.html',
                              extra_context={
                               'footer_tagline':"Because We're <em>Your &nbsp;</em>Family&trade;",
                               'poll':Poll.objects.all().order_by('-pub_date')[0]
                               },
                              )
