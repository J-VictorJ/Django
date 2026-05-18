from django.shortcuts import render, get_list_or_404, get_object_or_404
# from django.http import HttpResponse
from utils.recipes.factory import make_recipe
from . import views
from .models import Recipe
# Importing the HttpResponse function to return a simple HTTP response
#But in recipes.views



def home(request):
    recipes = Recipe.objects.filter(
        is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })
    
    
    
def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(category__id = category_id, is_published=True,).order_by("-id"))
    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name} - Category | '
    })



def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True,)
    return render(request, 'recipes/pages/recipe-view.html', context={
        #'name': 'я Виктор'
        'recipe': recipe,
        'is_detail_page': True,
    })

#def sobre(request):
#    return HttpResponse("\"Sobre\" a página de receitas")
    # return render(request, 'recipes/sobre.html')
    # This will render the 'sobre.html' template located in the 'recipes' app's templates directory