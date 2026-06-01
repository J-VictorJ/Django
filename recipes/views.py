from django.shortcuts import render, get_list_or_404, get_object_or_404
# from django.http import HttpResponse
# from utils.recipes.factory import make_recipe
# from . import views
from .models import Recipe
from django.http.response import Http404
from django.db.models import Q
from utils.pagination import make_pagination
import os
# from django.contrib import messages
# Importing the HttpResponse function to return a simple HTTP response
#But in recipes.views

PER_PAGES = int(os.environ.get('PER_PAGES', 6))

def home(request):
    recipes = Recipe.objects.filter(
        is_published=True).order_by('-id')
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)
    
    # messages.success(request, 'Success!!')
    
    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range
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


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)

    return render(request, 'recipes/pages/search.html', {
        'pages_title': f'Search for "{search_term}" | ',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    })
    
    
#def sobre(request):
#    return HttpResponse("\"Sobre\" a página de receitas")
    # return render(request, 'recipes/sobre.html')
    # This will render the 'sobre.html' template located in the 'recipes' app's templates directory