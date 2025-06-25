from django.http import HttpResponse
from django.urls import path
from recipes.views import home, sobre


urlpatterns = [
    path('', home),
    path('sobre/', sobre),
    # The 'sobre' path will return a simple HTTP response when accessed
]
