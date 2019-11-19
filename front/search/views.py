from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .forms import QueryForm

from .models import Query

# Create your views here.

def index(request):
    return render(request, 'search/index.html')

def result(request, query_id):
    q = Query.objects.get(pk=query_id)
    msg = "Book #" + str(query_id) + " is: " + str(q)

    bookRank = [
        {
            "title": "Oi",
            "author": "Ana",
            "url": "http://www.cin.ufpe.br"
        },
        {
            "title": "Tchau",
            "author": "Ana",
            "url": "http://www.ufpe.br"
        },
        {
            "title": "Nossa",
            "author": "Biu",
            "url": "http://www.siga.ufpe.br"
        },
        {
            "title": "OK",
            "author": "Biu",
            "url": "http://www.biblioteca.ufpe.br"
        },
    ]

    context = {
        "msg": msg,
        "bookRank": bookRank
    }

    #return HttpResponse(msg)
    return render(request, 'search/result.html', {"context": context})

def invalid(request):
    return render(request, 'search/invalid.html')

def allFieldsEmpty(queryData):
    for value in queryData.values():
        if(value != '' and value != None):
            return False
    return True

def getQueryForm(request):
    if request.method == 'POST':
        queryForm = QueryForm(request.POST)
        isValid = queryForm.is_valid()
        
        if(isValid):
            cleanedData = queryForm.cleaned_data
            ##print(cleanedData)
            empty = allFieldsEmpty(cleanedData)
            if(not empty):
                q = Query(cleanedData)
                ## make query model and get from database
                ## show result
                ## 
                ## tutorial:
                #     process the data in form.cleaned_data as required
                #     ...
                #     redirect to a new URL:
                ##    return HttpResponseRedirect('/thanks/')
                return HttpResponseRedirect('/search/result/1')
        
        return HttpResponseRedirect('/search/invalid/')