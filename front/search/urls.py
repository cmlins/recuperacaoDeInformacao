from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result/<str:data>/', views.result, name='result'),
    path('getBookForm/', views.getBookForm, name='getBookForm'),
    path('getBookQueryString/', views.getBookQueryString, name="getBookQueryString"),
    path('invalid/', views.invalid, name="invalid"),
    path('simple/', views.simple, name='simple')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)