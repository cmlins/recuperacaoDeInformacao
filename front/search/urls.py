from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result/<int:query_id>/', views.result, name='result'),
    path('getQueryForm/', views.getQueryForm, name='getQueryForm'),
    path('invalid/', views.invalid, name="invalid")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)