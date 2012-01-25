from django.shortcuts import render_to_response

from forms import CourseSearch
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
	
def calendar(request):
	
	return render_to_response('courses/course_base.html',
						{
						'form':CourseSearch()
						},
						)

def course_match(request):
	
	results = {}
	
	
	return render_to_response('courses/result_list.html',{'results':results, 'get':request.GET})