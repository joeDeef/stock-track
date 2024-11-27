from django.shortcuts import render

def compras(request):
    return render(request, 'comprar.html')