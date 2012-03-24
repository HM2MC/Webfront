from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.simple import direct_to_template
from django.views.decorators.csrf import csrf_exempt


from m2m.polls.models import Poll, Choice

# Create your views here.    

def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return direct_to_template('polls/index.html', {'latest_poll_list': latest_poll_list})

@user_passes_test(lambda u: u.has_perm('polls.can_add_poll'))
def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return direct_to_template(request, 'polls/detail.html', extra_context={'poll': p})

@login_required
def vote(request, poll_id):
    p = get_object_or_404(Poll,pk=poll_id)
    
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form
        return direct_to_template('polls/detail.html',{
            'object':p,
            'errror_message':"You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
        selected_choice.votes.add(request.user)
        selected_choice.save()
        
        return HttpResponseRedirect(reverse('poll_results',args=(p.id,)))
    
def get_latest_poll(request, n=0):
    try:
        p = Poll.objects.all().order_by('-pub_date')[n]
    except IndexError:
        p = "No more polls!"
        
#@login_required
def vote_by_form(request):
    """if request.is_ajax():
        p = get_object_or_404(Poll, pk=poll_id)
        try:
            c = p.choice_set.get(pk=choice_id)
        except:
            return HttpResponse(status=400)
        
        c.votes += 1
        c.users.add(request.user)
        p.has_voted.add(request.user)
        
        return HttpResponse(status=200)
    return HttpResponse(status=404)"""
    try:
        print request.GET
        print request.POST
        poll_id = int(request.GET['poll_id'])
        choice_id = int(request.GET['choice_id'])
        p = Poll.objects.get(pk=poll_id)
        c = Choice.objects.get(pk=choice_id)
        
        c.users.add(request.user)
        c.save()
        p.has_voted.add(request.user)
    except:
        print "Exception!"
        return HttpResponse(status=404)
    return render_to_response("ajax_response.html",
                              {
                              'poll': p
                              },
                              context_instance=RequestContext(request))
    
    