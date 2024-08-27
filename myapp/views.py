from django.contrib.auth import logout, login, authenticate
import requests
from datetime import datetime, timedelta
from collections import defaultdict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.conf import settings
from .models import FavoriteTeam, UserFavoriteTeam, UserReview, Team
import logging

API_KEY = '0a1f33042a81c173f168fad17044385f'
API_HOST = 'v3.football.api-sports.io'
HEADERS = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': API_HOST
}

logger = logging.getLogger(__name__)

def fetch_teams(query):
    url = f"https://{API_HOST}/teams"
    params = {'search': query}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

def fetch_venues(query):
    url = f"https://{API_HOST}/venues"
    params = {'search': query}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

def fetch_irish_premier_teams():
    url = f"https://{API_HOST}/teams"
    params = {'league': 357, 'season': 2024}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

def fetch_irish_premier_stadiums():
    url = f"https://{API_HOST}/venues"
    params = {'country': 'Ireland'}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

def search(request):
    query = request.GET.get('q', '')
    teams_response = fetch_teams(query)
    venues_response = fetch_venues(query)
    
    team = None
    stadiums = []
    no_ireland = False

    def add_stadium(stadium_data):
        for stadium in stadiums:
            if stadium['name'] == stadium_data['name']:
                return
        stadiums.append(stadium_data)

    if teams_response['results'] > 0:
        ireland_teams = [team for team in teams_response['response'] if team['team']['country'] == 'Ireland']
        if ireland_teams:
            team_data = ireland_teams[0]['team']
            venue_data = ireland_teams[0]['venue']
            
            team = {
                'name': team_data['name'],
                'country': team_data['country'],
                'logo': team_data['logo'],
                'founded': team_data['founded']
            }
            
            if venue_data:
                add_stadium({
                    'name': venue_data['name'],
                    'address': venue_data['address'],
                    'city': venue_data['city'],
                    'capacity': venue_data['capacity'],
                    'surface': venue_data['surface'],
                    'image': venue_data['image']
                })

    if venues_response['results'] > 0:
        ireland_venues = [venue for venue in venues_response['response'] if venue['country'] == 'Ireland']
        for venue_data in ireland_venues:
            add_stadium({
                'name': venue_data['name'],
                'address': venue_data['address'],
                'city': venue_data['city'],
                'capacity': venue_data['capacity'],
                'surface': venue_data['surface'],
                'image': venue_data['image']
            })

    if not team and not stadiums:
        no_ireland = True

    context = {
        'team': team,
        'stadiums': stadiums,
        'no_ireland': no_ireland
    }

    return render(request, 'search_results.html', context)

def fetch_fixtures_for_team(team_id):
    url = f"https://{API_HOST}/fixtures"
    params = {'team': team_id, 'season': 2024, 'next': 3}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        fixtures = response.json().get('response', [])
        return fixtures
    else:
        return []

def home(request):
    favorite_teams = []
    fixtures = []

    if request.user.is_authenticated:
        # Fetch the user's favorite teams
        user_favorite_teams = UserFavoriteTeam.objects.filter(user=request.user)
        if user_favorite_teams.exists():
            favorite_teams = [fav.team for fav in user_favorite_teams]
        
        print("Favorite Teams:", favorite_teams)  # Debug: print favorite teams

        # Fetch fixtures for favorite teams
        for team in favorite_teams:
            team_fixtures = fetch_fixtures_for_team(team.id)
            for fixture in team_fixtures:
                fixtures.append({
                    'home_team': fixture['teams']['home']['name'],
                    'away_team': fixture['teams']['away']['name'],
                    'date': fixture['fixture']['date']
                })
        
        print("Fixtures:", fixtures)  # Debug: print upcoming fixtures

    context = {
        'favorite_teams': favorite_teams,
        'fixtures': fixtures[:3],  # Only show next 3 fixtures
    }
    return render(request, 'home.html', context)


def team_detail(request, team_id):
    url = f"https://{API_HOST}/teams?id={team_id}"
    response = requests.get(url, headers=HEADERS)
    team = response.json()['response'][0] if response.json()['response'] else None

    context = {
        'team': team
    }
    return render(request, 'team_detail.html', context)

def stadiums(request):
    stadium_response = fetch_irish_premier_stadiums()
    stadiums = stadium_response['response'] if stadium_response['response'] else []
    
    context = {
        'stadiums': stadiums
    }
    return render(request, 'stadiums.html', context)

def fetch_irish_premier_fixtures():
    url = f"https://{API_HOST}/fixtures"
    params = {'league': 357, 'season': 2024}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

def fixtures(request):
    fixture_response = fetch_irish_premier_fixtures()
    fixtures = fixture_response['response'] if fixture_response['response'] else []

    current_date = datetime.utcnow().date()
    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    this_week_fixtures = []
    fixtures_by_round = defaultdict(list)

    for fixture in fixtures:
        fixture_date = datetime.strptime(fixture['fixture']['date'][:10], '%Y-%m-%d').date()
        if start_of_week <= fixture_date <= end_of_week:
            this_week_fixtures.append(fixture)
        round_name = fixture['league']['round']
        fixtures_by_round[round_name].append(fixture)

    context = {
        'this_week_fixtures': this_week_fixtures,
        'fixtures_by_round': dict(fixtures_by_round)
    }
    
    return render(request, 'fixtures.html', context)

def fetch_nearby_places(query, types):
    results = {}
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    for place_type in types:
        params = {
            "query": f"{query} {place_type}",
            "type": place_type,
            "key": settings.GOOGLE_API_KEY
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            results[place_type] = response.json().get('results', [])
    return results

def nearby_places(request, venue_name):
    types = ['restaurant', 'cafe', 'hotel', 'pub', 'parking', 'pharmacy', 'atm']
    places = fetch_nearby_places(venue_name, types)
    return render(request, 'nearby_places.html', {'places': places, 'venue_name': venue_name})

def teams(request):
    team_response = fetch_irish_premier_teams()
    teams = []
    for team in team_response.get('response', []):
        venue = team.get('venue', {})
        if venue.get('latitude') and venue.get('longitude'):
            teams.append(team)
        else:
            team['venue']['latitude'] = 'default_latitude'
            team['venue']['longitude'] = 'default_longitude'
            teams.append(team)

    # Get the IDs of the user's favorite teams
    favorite_team_ids = []
    if request.user.is_authenticated:
        favorite_team_ids = UserFavoriteTeam.objects.filter(user=request.user).values_list('team__id', flat=True)

    context = {
        'teams': teams,
        'favorite_team_ids': favorite_team_ids,  # Pass the list of favorite team IDs to the template
    }
    return render(request, 'teams.html', context)



@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account has been successfully deleted.")
        return redirect('home')
    return render(request, 'delete_account.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')

from django.contrib import messages

@login_required
def add_favorite_team(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        api_url = f"https://{API_HOST}/teams?id={team_id}"
        response = requests.get(api_url, headers=HEADERS)
        
        if response.status_code == 200:
            team_data = response.json().get('response', [])[0]
            team = Team.objects.create(
                id=team_data['team']['id'],
                name=team_data['team']['name'],
            )
        else:
            messages.error(request, "Team could not be found.")
            return redirect('home')
    
    favorite, created = UserFavoriteTeam.objects.get_or_create(user=request.user, team=team)
    if created:
        messages.success(request, f"{team.name} has been added to your favorites!")
    else:
        messages.info(request, f"{team.name} is already in your favorites.")

    return redirect('home')


@login_required
def favorites_list(request):
    user_favorites = UserFavoriteTeam.objects.filter(user=request.user)
    favorite_teams = [favorite.team for favorite in user_favorites]
    return render(request, 'favorites_list.html', {'favorites': favorite_teams})

from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

from django.shortcuts import get_object_or_404

@login_required
def remove_favorite_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    UserFavoriteTeam.objects.filter(user=request.user, team=team).delete()
    messages.success(request, f"{team.name} has been removed from your favorites.")
    return redirect('home')