from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('home/', views.home, name='home'),
    path('teams/', views.teams, name='teams'),
    path('teams/<int:team_id>/', views.team_detail, name='team_detail'),
    path('stadiums/', views.stadiums, name='stadiums'),
    path('fixtures/', views.fixtures, name='fixtures'),
    path('', views.home, name='home'),
    path('nearby-places/<str:venue_name>/', views.nearby_places, name='nearby_places'),
]
