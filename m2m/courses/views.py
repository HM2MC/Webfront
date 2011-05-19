from django.shortcuts import render_to_response

# Create your views here.

def index(request):

	return render_to_response("courses/index.html",
						{
						},)

def browse(request):
	
	return render_to_response("courses/menus.html",
						{
						},)
						
def search(request, q=''):
	
	return render_to_response('courses/result.html',
						{
						}
						,)