from django.urls import path

from . import views

urlpatterns = [
    path('terms-and-conditions', views.terms_and_conditions, name='t&c'),
    path('query/<str:query_secret>', views.query, name='query'),
    path('', views.home),
]
