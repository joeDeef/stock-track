from django.shortcuts import render
from django.template import TemplateDoesNotExist

def nosotros(request):
    try:
        return render(request, 'nosotros.html')
    except TemplateDoesNotExist:
        return render(request, 'error.html', status=404)