from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .forms import BookForm

from .models import BookQuery

import random
import pandas as pd
import numpy as np
import math

from bs4 import BeautifulSoup as bs
from bs4 import UnicodeDammit

# Create your views here.

def index(request):
    return render(request, 'search/index.html')

def result(request, data):
    
    ranking = None
    
    query = json.loads(data)
    if isinstance(query, dict):
        ranking = processQueryDict(query)
    else:
        ranking = processQueryString(query)

    """q = BookQuery.objects.get(pk=query_id)
    msg = "Book #" + str(query_id) + " is: " + str(q)"""

    """bookRank = [
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
    ]"""

    alsoSee = makeRecomendations()

    context = {
        "msg": msg,
        "bookRank": bookRank,
        "alsoSee": alsoSee
    }
    

    #return HttpResponse(msg)
    return render(request, 'search/result.html', {"context": context})

def invalid(request):
    return render(request, 'search/invalid.html')

def simple(request):
    return render(request, 'search/simple.html')

def allFieldsEmpty(queryData):
    for value in queryData.values():
        if(value != '' and value != None):
            return False
    return True

def getBookQueryString(request):
    if request.method == 'POST':
        bookForm = BookForm(request.POST)
        isValid = bookForm.is_valid()
        queryStr = ''

        if(isValid):
            cleanedData = bookForm.cleaned_data
            queryStr = cleanedData['anything']
            if queryStr != '':
                result = processQueryString(queryStr)
                ## aaaaa
                return HttpResponseRedirect('/search/result/1')
        
        return HttpResponseRedirect('/search/result/invalid')
                
def makeRecomendations():

    df = pd.read_csv('search/csvs/table.csv')
    randomIndices = random.sample(range(len(df.index)), 10)
    randomDocs = df.iloc[randomIndices]
    
    return randomDocs.to_json(force_ascii=False)

def getBookForm(request):
    if request.method == 'POST':
        bookForm = BookForm(request.POST)
        isValid = bookForm.is_valid()
        
        if(isValid):
            cleanedData = bookForm.cleaned_data
            empty = allFieldsEmpty(cleanedData)
            if(not empty):
                queryDict = dict(cleanedData)
                if not q.author:
                    queryDict.pop('author')
                if not q.title:
                    queryDict.pop('title')
                if not q.isbn:
                    queryDict.pop('isbn')
                if not q.language:
                    queryDict.pop('language')
                if not q.publisher:
                    queryDict.pop('publisher')
                
                query_json = json.dumps(queryDict, ensure_ascii=False).encode('utf8').decode()
                
                ## result = processQueryDict(queryDict)
                
                return HttpResponseRedirect('/search/result/' + query_json)
        
        return HttpResponseRedirect('/search/invalid/')

def processQueryString(queryStr):
    df_fs = free_search(fq, df_indice) 
    dl_fs = docs_list_OR(df_fs)
    
    df_tfidf_fs = calc_freq(dl_fs, df_fs, 'livre', fq)
    df_tfidf_fs = calc_tfidf(df_tfidf_fs)
    r_tfidf_fs = calc_rank(df_tfidf_fs, handlingQuery(fq), 'livre')
    rd_tfidf_fs = ranking_dictionary(r_tfidf_fs)
    
    return rd_tfidf_fs
    
def processQueryDict(queryDict):
    df_ss = structured_search(queryDict, df_campos)
    dl_ss = docs_list_OR(df_ss)

    df_tfidf_ss = calc_freq(dl_ss, df_ss, 'estruturada', sq)
    df_tfidf_ss = calc_tfidf(df_tfidf_ss)
    r_tfidf_ss = calc_rank(df_tfidf_ss, getValues(sq), 'estruturada')
    rd_tfidf_ss = ranking_dictionary(r_tfidf_ss)
    
    return rd_tfidf_ss

"""                          ~~~~
  ______ _    _ _   _  _____ ____  ______  _____ 
 |  ____| |  | | \ | |/ ____/ __ \|  ____|/ ____|
 | |__  | |  | |  \| | |   | |  | | |__  | (___  
 |  __| | |  | | . ` | |   | |  | |  __|  \___ \ 
 | |    | |__| | |\  | |___| |__| | |____ ____) |
 |_|     \____/|_| \_|\_____\____/|______|_____/ 
                        )_)                         
"""

df_ed = pd.read_csv('search/csvs/dfs_tot.csv')

symbolsToReplace = [
    '(', ')', '!', '?', ':', ';', '*', '.', ',', '★', '|', '+', '[', ']', '{', '}', '/', 'ª', 'º', '°', '-',
    '%', '—', '@', '#',  '\"', '\'', '<', '>', '=', '´', '`', '“', '$', '&', '’', '¡', '€', 'µ', '¦',
    '\\', '®', '™', '”', '…', '‘', '•', '😍', '😙', '❤', '–', '⭐️', '_', '️⭐', '😉', '👏', '¹', '²', '³',
    "£", '¢', '¬', '§', '~', '^', '×', '÷',
    '\u200c', '\u200f', '\u200e', '\t', '\xa0', '\x03', '\u0301', '\u0303'
]

allowedSmallTokens = [
    # acabei de perceber que 'não' nem tá aqui kkkkk
    'fio', 'box', 'god', 'key', 'bit', 'led', 'faq', 'dog', 'sim', 'ovo', 'pão', 'aba', 'new'
]

def getAndCleanHTML(filepath):

    page = open(filepath, "rb")

    page = page.read()

    clearPage = UnicodeDammit.detwingle(page)

    doc = bs(clearPage, 'lxml')

    for script in doc(["script", "style"]):
        script.extract()

    docText = doc.get_text(' ')

    # é essa aqui que remove os números <------------
    docText = docText.translate({ord(ch): None for ch in '0123456789'})

    docText = docText.lower()

    docText = docText.replace("e-book", "ebook")

    docText = docText.replace("blu-ray", "bluray")

    for symbol in symbolsToReplace:
        docText = docText.replace(symbol, ' ')

    docText = docText.replace("  ", ' ')

    lines = (line.strip() for line in docText.splitlines())

    chunks = (phrase.strip() for line in lines for phrase in line.split(' '))

    text = ' '.join(chunk for chunk in chunks if chunk)

    return text

def handlingQuery(query):
    hq = query.split()
    return hq


def getValues(query):
    rl = list()
    for i in query:
        wl = query[i].split(' ')
        for w in wl:
            rl.append(w)
    return rl


def free_search(q, indice):
    hq = handlingQuery(q)
    df_search = pd.DataFrame()
    for q in hq:
        for w in indice['Terms'].values:
            if (w in q) or (w == q):
                df_search = df_search.append(
                    indice[indice['Terms'] == w], ignore_index=True)
    return df_search


def structured_search(sq, indice):
    df_search = pd.DataFrame()
    for i in sq:
        values_sq = sq[i].split(' ')
        for v in values_sq:
            for r in range(len(df_campos)):
                sr = df_campos.at[r, 'Field Text'].split('.')
                if (sr[0] in v) and (sr[1] == i):
                    df_search = df_search.append(
                        df_campos[df_campos['Field Text'] == sr[0] + '.' + sr[1]], ignore_index=True)
    return df_search


def docs_list_OR(df):
    postings = list()
    for r in df.index:
        postings.append(df.loc[r, 'Posting'])

    for i in range(len(postings)):
        new_postings = postings[i].split(', ')
        new_postings[0] = new_postings[0][1:]
        new_postings[len(new_postings) -
                     1] = new_postings[len(new_postings)-1][:-1]
        postings[i] = new_postings

    p = list()
    for i in range(len(postings)):
        for j in range(len(postings[i])):
            p.append(postings[i][j])

    p = list(dict.fromkeys(p))
    return p


def docs_list_AND(df):
    aux = list()
    postings_list = list()
    # colocar postings em listas
    for r in df.index:
        aux = df.at[r, 'Posting'].split(', ')
        aux[0] = aux[0][1:]
        aux[len(aux)-1] = aux[len(aux)-1][:-1]
        postings_list.append(aux)

    # iterar sobre listas de postings buscando itens iguais
    postings = list()
    for i in range(len(postings_list)):
        for j in range(i+1, len(postings_list)):
            for k in range(len(postings_list[i])):
                for l in range(len(postings_list[j])):
                    if postings_list[i][k] == postings_list[j][l]:
                        postings.append(postings_list[i][k])
                        postings_list[i][j] = ' '

    return postings


"""## Calc Scores"""


def calc_tfidf(df_freq):
    for r in df_freq.index:
        df_freq.at[r, 'Freq'] = math.log(
            df_arquivos.shape[0]/df_freq.at[r, 'Freq'], 10)
        for c in range(2, len(df_freq.columns)):
            df_freq.iloc[r, c] = np.multiply(
                df_freq.at[r, 'Freq'], df_freq.iloc[r, c])

    return df_freq


def calc_freq(dl, df_search, tipo_busca, q):
    df_freq = pd.DataFrame(columns=dl)
    if tipo_busca == 'livre':
        df_freq = pd.concat(
            [df_search['Terms'], df_search['Freq'], df_freq], axis=1)
        queryl = handlingQuery(q)
    else:
        queryl = getValues(q)
        df_freq = pd.concat(
            [df_search['Field Text'], df_search['Freq'], df_freq], axis=1)

    for r in df_freq.index:
        for c in range(2, len(df_freq.columns)):
            df_freq.iloc[r, c] = 0

    df_freq.iloc[:, 1:] = df_freq.iloc[:, 1:].astype(float)

    for i in range(len(dl)):
        doc = getAndCleanHTML(df_arquivos.loc[int(dl[i]), '0'])
        doc = doc.lower()
        doc = doc.split()
        for w in doc:
            for qw in range(len(queryl)):
                if w == queryl[qw]:
                    df_freq.at[qw, dl[i]] += 1.0

    for r in df_freq.index:
        for c in range(2, len(df_freq.columns)):
            if df_freq.at[r, df_freq.columns[c]] != 0:
                df_freq.at[r, df_freq.columns[c]] = math.log10(
                    df_freq.at[r, df_freq.columns[c]])

    return df_freq


"""## Calc Ranking"""


def calc_rank(df_freq, hq, tipo_busca):
    if tipo_busca == 'livre':
        df_freq.at[len(df_freq.index), 'Terms'] = 'cosine'
        df_freq.index = df_freq['Terms']
    else:
        df_freq.at[len(df_freq.index), 'Field Text'] = 'cosine'
        df_freq.index = df_freq['Field Text']

    df_freq = df_freq.iloc[:, 1:]

    dv = []
    qv = []
    for q in hq:
        qv.append(1)

    for c in range(1, len(df_freq.columns)):
        for r in range(len(df_freq.index[:-1])):
            dv.append(df_freq.iloc[r, c])
        df_freq.iloc[len(df_freq.index)-1, c] = (np.dot(dv, qv) /
                                                 (np.linalg.norm(dv) * np.linalg.norm(qv)))
        dv = []

    df_rank = df_freq.sort_values(by='cosine', axis=1, ascending=False)
    df_rank = df_rank.drop(['Freq'], axis=1)
    ranking = df_rank.columns.tolist()
    ranking = ranking[:10]
    return ranking


def ranking_dictionary(r):
    rd_list = list()
    for i in r:
        path = df_arquivos.at[int(i), '0']
        row, = df_ed[df_ed['Documento'] == path].index
        titulo = df_ed.at[row, 'Título']
        autor = df_ed.at[row, 'Autor']
        rd = {
            'index': i,
            'title': titulo,
            'author': autor
        }
        rd_list.append(rd)

    return rd_list
""" FIM DAS FUNÇÕES"""

""" COMO CHAMAR 

df_indice = pd.read_csv('search/csvs/indice_inv.csv')
df_arquivos = pd.read_csv('search/csvs/urls_df.csv')
df_campos = pd.read_csv('search/csvs/field_texts.csv')

## busca livre ##
fq = 'diário garoto'
df_fs = free_search(fq, df_indice) 
dl_fs = docs_list_OR(df_fs)

## tf
df_f_fs = calc_freq(dl_fs, df_fs, 'livre', fq)
r_f_fs = calc_rank(df_f_fs, handlingQuery(fq), 'livre')
rd_f_fs = ranking_dictionary(r_f_fs)

# tfidf
df_tfidf_fs = calc_freq(dl_fs, df_fs, 'livre', fq)
df_tfidf_fs = calc_tfidf(df_tfidf_fs)
r_tfidf_fs = calc_rank(df_tfidf_fs, handlingQuery(fq), 'livre')
rd_tfidf_fs = ranking_dictionary(r_tfidf_fs)

sq = {
    'title': 'sítio amarelo',
    'author': 'monteiro lobato',
}
df_ss = structured_search(sq, df_campos)
dl_ss = docs_list_OR(df_ss)

## tf
df_f_ss = calc_freq(dl_ss, df_ss, 'estruturada', sq)
r_f_ss = calc_rank(df_f_ss, getValues(sq), 'estruturada')
rd_f_ss = ranking_dictionary(r_f_ss)

## tfidf
df_tfidf_ss = calc_freq(dl_ss, df_ss, 'estruturada', sq)
df_tfidf_ss = calc_tfidf(df_tfidf_ss)
r_tfidf_ss = calc_rank(df_tfidf_ss, getValues(sq), 'estruturada')
rd_tfidf_ss = ranking_dictionary(r_tfidf_ss)

"""
