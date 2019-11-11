from django.shortcuts import render
from django.http import HttpResponse
##from django.template import loader

from .models import Query

# Create your views here.

def index(request):
    ##template = loader.get_template('search/index.html')
    context = {

    }
    return render(request, 'search/index.html')
    ##return HttpResponse(template.render(context, request))
    ##return HttpResponse("Hello, world! Welcome to the search page.")

def result(request, query_id):
    q = Query.objects.get(pk=query_id)
    msg = "Book #" + str(query_id) + " is: " + str(q)
    return HttpResponse(msg)