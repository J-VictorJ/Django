from django.shortcuts import render, redirect
from authors.forms import RegisterForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from authors.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
# from authors.forms.recipe_form import AuthorRecipeForm
# Create your views here.
def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html',{
        'form': form,
        'form_action': reverse('authors:register_create'),
    })

def register_create(request):
    if not request.POST:
        raise Http404
    
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)
    
    if form.is_valid():
        user = form.save()
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is created, please log in :)')
        
        del(request.session['register_form_data'])
        return redirect(reverse('authors:login'))
    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
                  'form': form,
                  'form_action': reverse('authors:login_create')
                  })


def login_create(request):
    if not request.POST:
        raise Http404()
    
    form = LoginForm(request.POST)
    
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        
        if authenticated_user is not None:
            messages.success(request, 'You are Logged in') 
            login(request, authenticated_user)
        else:
            messages.error(request, "INVALID CREDENTIALS!")
    else:
        messages.error(request, 'Error to validate form data')
   
    return redirect(reverse('authors:dashboard'))


"""from django.db import connection
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

# (todos os imports originais continuam no topo do arquivo)
@csrf_exempt
def login_create(request):
    if not request.POST:
        raise Http404()

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    # ⚠️ VULNERÁVEL (proposital)
    # Query montada por concatenação — sem parametrização
    sql = (
        "SELECT id, username, password, email "
        "FROM auth_user "
        f"WHERE username = '{username}' AND password = '{password}'"
    )

    resultado = None
    erro_sql = None

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            resultado = cursor.fetchall()
    except Exception as exc:
        erro_sql = str(exc)

    if resultado:
        user = User.objects.get(pk=resultado[0][0])
        login(request, user)
        messages.success(request, f'Logado como {resultado[0][1]}')

    return render(request, 'authors/pages/login.html', {
        'form': LoginForm(),
        'form_action': reverse('authors:login_create'),
        'query': sql,
        'resultado': resultado,
        'erro_sql': erro_sql,
    })
"""
@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect(reverse('authors:login'))

    messages.success(request, 'Logged out successfully')
    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published = False,
        author=request.user
    )
    return render(request, 'authors/pages/dashboard.html',
                  context={
                      'recipes': recipes,
                  })
