from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', views.search, name='search'),
    path('', views.home, name='home'),  
    path('home/', views.home, name='home'),  
    path('teams/', views.teams, name='teams'),
    path('teams/<int:team_id>/', views.team_detail, name='team_detail'),
    path('stadiums/', views.stadiums, name='stadiums'),
    path('standings/', views.standings, name='standings'),
    path('fixtures/', views.fixtures, name='fixtures'),
    path('nearby-places/<str:venue_name>/', views.nearby_places, name='nearby_places'),
    path('register/', views.register, name='register'),
    
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('delete-account/', views.delete_account, name='delete_account'),
    path('add_favorite_team/<int:team_id>/', views.add_favorite_team, name='add_favorite_team'),
    path('remove_favorite_team/<int:team_id>/', views.remove_favorite_team, name='remove_favorite_team'),

    path('favorites/', views.favorites_list, name='favorites_list'),
    
    path('accounts/', include('django.contrib.auth.urls')),
    path('venues/<int:venue_id>/', views.venue_detail, name='venue_detail'),
    path('venues/<int:venue_id>/add_review/', views.add_stadium_review, name='add_stadium_review'),  
]

