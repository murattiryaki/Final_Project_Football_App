from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
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

    path('admin/', admin.site.urls),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('delete-account/', views.delete_account, name='delete_account'),

    path('accounts/', include('accounts.urls')),
]
