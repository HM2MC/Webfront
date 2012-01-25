from django.shortcuts import render_to_response
# Create your views here.
import urllib2

def main(request):
    resp = urllib2.urlopen("http://www.cafebonappetit.com/menu/your-cafe/pitzer/cafes/details/219/mcconnell-bistro")
    return render_to_response('menu/main.html',{})