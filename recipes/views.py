from django.shortcuts import render
from django.http import HttpResponse

# Importing the HttpResponse function to return a simple HTTP response
#But in recipes.views

def home(request):
    return render(request, 'home.html', { 'name': 'я Виктор'})

def sobre(request):
    return HttpResponse("\"Sobre\" a página de receitas")
    # return render(request, 'recipes/sobre.html')
    # This will render the 'sobre.html' template located in the 'recipes' app's templates directory