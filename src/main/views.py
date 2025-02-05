from django.shortcuts import render
from django.template import TemplateDoesNotExist

def inicio(request):
    try:
        return render(request, 'index.html')  # Renderiza el archivo HTML desde la carpeta "templates"
    except TemplateDoesNotExist:
        return render(request, 'error.html', status=404)