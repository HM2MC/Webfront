from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
#from django.db import transaction

from models import Comment
from formClasses import RequestForm, ModifyForm

from datetime import datetime
# Set some nice globals here
PERPAGE = 20 # how many requests per page?

# Create your views here.

def open(request,page=1,error=''):
    '''Handles the display of the open request. Seriously, this isn't rocket science or anything.'''
      
    try:
        page = int(page) - 1 # switch to zero indexing
        if page < 0:
            page = 0
    except Exception:
        page = 0

    # different behavior if a request was submitted
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            try:
                #from django.db import connection
    
                #cursor = connection.cursor()
                #cursor.execute('LOCK TABLES requests_comment WRITE')
                try:
                    reqip = request.META['HTTP_X_REAL_IP']
                except:
                    reqip = request.META['REMOTE_ADDR']
                if request.user.is_authenticated():
                    user = request.user
                else:
                    user = None
                newRequest = Comment(
                                request=form.cleaned_data['request'],
                                name=form.cleaned_data['name'],
                                server=form.cleaned_data['server'].upper(),
                                email=form.cleaned_data['email'],
                                requestIP=reqip,
                                requestTime = datetime.now(),
                                user=user
                                )
                
                newRequest.save()
                #cursor.execute('UNLOCK TABLES')
                # successful post, return to requests page to see the result
                
                '''
#########################################################
# --- Log new request info 
#
                rom django.db import connection
                cursor = connection.cursor()
                
                cursor.execute('LOCK TABLES log, requests_comment WRITE')
                cursor.execute(
                    'INSERT INTO log (Time,Client,SearchString)\
                    VALUES (%(time)d, "%(client)s", "%(search)s")' % {
                        'time':time.mktime(time.localtime()),
                        'client': reqip,
                        'search':"Request: %(query)s" % {'query':newRequest.request},
                    }
                )
                cursor.execute('UNLOCK TABLES')
                transaction.set_dirty()
                transaction.commit()
#
#
#########################################################
                '''
                
                test = 3
                return HttpResponseRedirect(reverse('request.views.open',args=(1,)))
            except Exception, e:
                form.non_field_errors = e
                test = 2
        else:
            test = 1
    else:
        form = RequestForm()
        test = 0
    #SQL: "SELECT * FROM comments WHERE COMPLETED = False AND deleted = False ORDER BY Time DESC LIMIT %(start)s,%(depth)s"%{'start':page*20, 'depth':PERPAGE}
    
    displaySet = Comment.objects.filter(isDeleted=0,completed=0).order_by('-requestTime')  # filter out deleted and completed, order by time
    setLen = len(displaySet)
    
    displaySet = displaySet[page*PERPAGE:(page+1)*PERPAGE]# and take the appropriate slice
    
    remainder = setLen % PERPAGE # we need to do this because setLen and PERPAGE are ints
    if remainder > 0:
        remainder = 1
    linkPages = range(1,setLen/PERPAGE + remainder + 1)
        

    
    return render_to_response('requests/requests.html',
                              {
                                'title':'M2M - Requests',
                                'requests':'current',
                                'openReq':'current', 
                                'displaySet':displaySet,
                                'toprequests': Comment.objects.filter(isDeleted=0,completed=0,likes__gt=0).order_by('-likes')[:PERPAGE+10],
                                'page':page+1,
                                'linkPages':linkPages,
                                'setLen':setLen,
                                'test':test,
                                'form':form,
                                'error':error,
                              },context_instance=RequestContext(request)
                              )

def completed(request,page=1):
    try: page = int(page) - 1
    except Exception:
        page = 0

    
    #SQL: "SELECT * FROM comments WHERE Completed = True AND deleted = False ORDER BY CompletedTime DESC LIMIT %(start)s,%(depth)s"%{'start':page*20,'depth':PERPAGE}

    displaySet = Comment.objects.filter(isDeleted=0,completed=1).order_by('-completedTime')  # filter out deleted and not-completed, order by completedtime
    setLen = len(displaySet)
    
    displaySet = displaySet[page*PERPAGE:(page+1)*PERPAGE]# and take the appropriate slice
    
    remainder = setLen % PERPAGE # we need to do this because setLen and PERPAGE are ints
    if remainder > 0:
        remainder = 1
    linkPages = range(1,setLen/PERPAGE + remainder + 1)    

    return render_to_response('requests/requests.html',
                          {
                            'title':'M2M - Completed Requests',
                            'requests':'current',
                            'closedReq':'current',
                            'modifier':'/completed',
                            'linkPages':linkPages,
                            'page':page+1,
                            'setLen':setLen,
                            'displaySet':displaySet,
                          })


def deleted(request,page=1):
    try: page = int(page) - 1
    except Exception:
        page = 0
        
    #SQL: "SELECT * FROM comments WHERE deleted = True ORDER BY Time DESC LIMIT %(start)s,%(depth)s"%{'start':page*20,'depth':PERPAGE}
    displaySet = Comment.objects.filter(isDeleted=1).order_by('-deletedTime')  # filter out not deleted, order by time
    setLen = len(displaySet)
    
    displaySet = displaySet[page*PERPAGE:(page+1)*PERPAGE]# and take the appropriate slice
    
    remainder = setLen % PERPAGE # we need to do this because setLen and PERPAGE are ints
    if remainder > 0:
        remainder = 1
    linkPages = range(1,setLen/PERPAGE + remainder + 1)    
    
    return render_to_response('requests/requests.html',
                          {
                            'title':'M2M - Deleted Requests',
                            'requests':'current',
                            'delReq':'current',
                            'modifier': '/deleted',
                            'linkPages':linkPages,
                            'page':page+1,
                            'setLen':setLen,
                            'displaySet':displaySet,
                          },context_instance=RequestContext(request))
    

def edit(request,id):
    
    entry = Comment.objects.get(pk=id)
    
    if entry.isDeleted or entry.completed: # no editing completed or deleted things!
        return HttpResponseRedirect(reverse('request.views.open',args=(1,)))
    
    
    if request.method == "POST":
        form = ModifyForm(request.POST,{'completingServer':"",})
        form.completingServer = ""
        if form.is_valid():
            test = 0
            #from django.db import connection
    
            #cursor = connection.cursor()
            #cursor.execute('LOCK TABLES requests_comment WRITE')
            
            entry.request = form.cleaned_data['request']
            entry.name = form.cleaned_data['name']
            entry.server = form.cleaned_data['server'].upper()
            entry.email = form.cleaned_data['email']
            entry.requestTime=datetime.now()
            
            entry.save()
            #cursor.execute('UNLOCK TABLES')
            return HttpResponseRedirect(reverse('request.views.open',args=(1,)))
        test = form.errors
    else:
        form = ModifyForm(instance=entry,initial={'completingServer':""})
        test = 1
    
    return render_to_response('requests/modify.html',
                              {
                                'title': 'M2M - Editing Request '+id,
                                'requests':'current',
                                'openReq':'current',
                                'entry':entry,
                                'edit':True,
                                'form':form,
                                'test':test,
                                },context_instance=RequestContext(request)
                              )
    
def complete(request,id):
    from django.core.mail import send_mail

    entry = Comment.objects.get(pk=id)
    
    if entry.isDeleted or entry.completed: # no double completes! nor completing deleted things.
        return HttpResponseRedirect(reverse('request.views.completed',current_app='requests'))
    
    if request.method == 'POST':
        form = ModifyForm(request.POST)
        if form.is_valid():
            if len(form.cleaned_data['completingServer']) > 0:
                try:
                    
                    entry.completed = True
                    entry.completingName = form.cleaned_data['completingName']
                    if len(form.cleaned_data['completingServer']) > 1:
                        entry.completingServer = form.cleaned_data['completingServer'].upper().replace('\\','')
                    else:
                        entry.completingServer = request.META['REMOTE_ADDR']
                    entry.completerComment = form.cleaned_data['completerComment']
                
                    entry.completedTime = datetime.now()
                    
                    entry.save()
                    
                    recipients = ['haak.erling@gmail.com']
                    if entry.email:
                        recipients += [entry.email]
                    elif entry.user:
                        recipients += [entry.user.email]
                        
                    message = "From %(host)s:\n\n%(completercomment)s\n\nEnjoy!\n\n This is an automated message; please do not reply to this address" % {'host':entry.completingServer,'completercomment':entry.completerComment}
                    try:
                        send_mail('Request Completed!',
                                  message,
                                  'requests@m2m.st.hmc.edu',
                                  recipients,
                                  )
                    except:
                        pass
                    test = 3
                    return HttpResponseRedirect(reverse('request.views.completed',current_app='requests'))
                except Exception,e:
                    form.non_field_errors = e
                    test = 2
        else:
            test = 1
    else:
        form = ModifyForm(instance=entry)
        test = 0
        
    return render_to_response('requests/modify.html',
                              {'title':'M2M - Completing Request '+id,
                               'requests':'current',
                               'closedReq':'current',
                               'entry':entry,
                               'complete':True,
                               'test':test,
                               'form':form,
                               },context_instance=RequestContext(request)
                              )
    
def delete(request,id):
    try:
        #from django.db import connection
    
        #cursor = connection.cursor()
        #cursor.execute('LOCK TABLES requests_comment WRITE')
        
        entry = Comment.objects.get(pk=id)
        entry.isDeleted = True
        entry.deleterIP = request.META['REMOTE_ADDR']
        entry.deletedTime = datetime.now()
        
        entry.save() 
        #cursor.execute('UNLOCK TABLES')
        return HttpResponseRedirect(reverse('request.views.open',current_app='requests'))
    except SyntaxError:
        
        return HttpResponseRedirect(reverse('request.views.open',args=(2,),current_app='requests'))


def like(request,id='q',page='q'):
    if not request.user.is_authenticated():
        return HttpResponseForbidden("You need to be logged in for that")
    try:
        entry = Comment.objects.get(pk=id)
        
        # keep track of who's liking what
        if request.user != entry.user:
            if request.user in entry.likers.all():
                entry.likers.remove(request.user)
            else:
                entry.likers.add(request.user)
        
        print 'added {} as likers of {}'.format(request.user, id)
        
        return HttpResponseRedirect(reverse('request.views.open',current_app='requests'))
    except:
        entry = None
    finally:
        return HttpResponseRedirect(reverse('request.views.open',current_app='requests'))
        
