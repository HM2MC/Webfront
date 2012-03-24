from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as authlogout
from django.template import RequestContext
from django.utils.html import escape

# Create your views here.

from forms import LoginForm

from datetime import datetime

from m2m.polls.models import Poll
from m2m.request.formClasses import RequestForm
from m2m.request.models import Comment


@login_required
def view_home(request):
    """Displays the user's home page.
    
    Currently ties into the request app's form to allow new requests to be made from this page.
    """
    if request.method == 'POST':
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            try:
                reqip = request.META['HTTP_X_REAL_IP']
            except:
                reqip = request.META['REMOTE_ADDR']
            if request.user.is_authenticated():
                user = request.user
            else:
                user = None
            newRequest = Comment(
                            request=request_form.cleaned_data['request'],
                            name=request_form.cleaned_data['name'],
                            server=request_form.cleaned_data['server'].upper(),
                            email=request_form.cleaned_data['email'],
                            requestIP=reqip,
                            requestTime = datetime.now(),
                            user=user
                            )
            
            newRequest.save()
  
    request_form = RequestForm()
        
    return direct_to_template(request, 'home.html',
                              extra_context={
                               'footer_tagline':"Because We're <em>Your &nbsp;</em>Family&trade;",
                               'poll':Poll.objects.all().order_by('-pub_date')[0],
                               'request_form':request_form,
                               },
                              )
@login_required
def inline_editable(request):
    """Handles editing for inline-edits.
    
    Requres a POSTed request object. 
    """
    if request.method != "POST":
        return HttpResponse("Not a posted form!")
    
    user = request.user
    id = request.POST['id']
    value = request.POST['value']
    
    if id == 'nname_edit':
        user.profile.nname = escape(value)
        user.profile.save()
        

    
