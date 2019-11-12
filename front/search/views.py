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
    return HttpResponse(msg)

def invalid(request):
    return render(request, 'search/invalid.html')

def allFieldsEmpty(queryData):
    str = ''
    for value in queryData.values():
        print(str, value)
        str = str or value
    return str == ''

def getQueryForm(request):
    if request.method == 'POST':
        queryForm = QueryForm(request.POST)
        isValid = queryForm.is_valid()
        
        if(isValid):
            cleanedData = queryForm.cleaned_data
            empty = allFieldsEmpty(cleanedData)
            if(not empty):
                q = Query(title='Oi', isbn='3423434', author='Joao da Silva', 
                        pages=123, publisher='DaMae', language='PTBR', 
                        coverType='capa dura')
                ## make query model and get from database
                ## show result
                ## do tutorial:
                #     process the data in form.cleaned_data as required
                #     ...
                #     redirect to a new URL:
                ##    return HttpResponseRedirect('/thanks/')
                return HttpResponseRedirect('/search/result/1')
        
        return HttpResponseRedirect('/search/invalid/')