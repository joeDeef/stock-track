from django.urls import path
from . import views

app_name = 'portafolio'

urlpatterns = [
    path('', views.get_portafolio, name='portafolio'),  
]
