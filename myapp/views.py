from django.contrib.auth import logout, login, authenticate
import requests
from datetime import datetime, timedelta
from collections import defaultdict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.conf import settings
from .models import UserFavoriteTeam, Team
import logging

API_KEY = 'ce72156581msh3d6327dd4145615p155153jsn227025ba1b7f'
API_HOST = 'api-football-v1.p.rapidapi.com/v3'
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

    if request.user.is_authenticated:
        favorite_teams = request.user.favorite_teams.all()
        favorite_team_ids = [fav.team.id for fav in favorite_teams]
    else:
        favorite_team_ids = []

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
                'id': team_data['id'],
                'name': team_data['name'],
                'country': team_data['country'],
                'logo': team_data['logo'],
                'founded': team_data['founded']
            }
            
            if venue_data:
                add_stadium({
                    'id': venue_data['id'],
                    'name': venue_data['name'],
                    'address': venue_data['address'],
                    'city': venue_data['city'],
                    'capacity': venue_data['capacity'],
                    'surface': venue_data['surface'],
                    'image': venue_data['image']
                })

    ireland_venues = [venue for venue in venues_response['response'] if venue['country'] == 'Ireland']
    for venue in ireland_venues:
        add_stadium({
            'id': venue['id'],
            'name': venue['name'],
            'address': venue.get('address', ''),
            'city': venue.get('city', ''),
            'capacity': venue.get('capacity', 0),
            'surface': venue.get('surface', ''),
            'image': venue.get('image', '')
        })

    context = {
        'team': team,
        'stadiums': stadiums,
        'favorite_team_ids': favorite_team_ids,
    }
    return render(request, 'search_results.html', context)

def fetch_fixtures_for_team(team_id):
    url = f"https://{API_HOST}/fixtures"
    params = {'team': team_id, 'season': 2024, 'next': 5}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        fixtures = response.json().get('response', [])
        return fixtures
    else:
        return []

from datetime import datetime

def home(request):
    favorite_teams = []
    fixtures = []

    if request.user.is_authenticated:
        
        user_favorite_teams = UserFavoriteTeam.objects.filter(user=request.user)
        if user_favorite_teams.exists():
            favorite_teams = [fav.team for fav in user_favorite_teams]

        print("Favorite Teams:", favorite_teams)  

        
        for team in favorite_teams:
            team_fixtures = fetch_fixtures_for_team(team.id)
            if team_fixtures:
                
                fixture = team_fixtures[0]  
                fixture_date = datetime.strptime(fixture['fixture']['date'], '%Y-%m-%dT%H:%M:%S%z')
                formatted_date = fixture_date.strftime('%d/%m/%Y %H:%M')

                fixtures.append({
                    'home_team': fixture['teams']['home']['name'],
                    'away_team': fixture['teams']['away']['name'],
                    'date': formatted_date,  
                    'referee': fixture['fixture'].get('referee', 'N/A'),
                    'home_logo': fixture['teams']['home']['logo'],
                    'away_logo': fixture['teams']['away']['logo'],
                    'result': f"{fixture['goals']['home']} - {fixture['goals']['away']}"
                })

        
        while len(fixtures) < 3 and len(favorite_teams) > 0:
            for team in favorite_teams:
                team_fixtures = fetch_fixtures_for_team(team.id)
                if team_fixtures and len(fixtures) < 3:
                    fixture = team_fixtures[1]  
                    fixture_date = datetime.strptime(fixture['fixture']['date'], '%Y-%m-%dT%H:%M:%S%z')
                    formatted_date = fixture_date.strftime('%d/%m/%Y %H:%M')

                    fixtures.append({
                        'home_team': fixture['teams']['home']['name'],
                        'away_team': fixture['teams']['away']['name'],
                        'date': formatted_date,  
                        'referee': fixture['fixture'].get('referee', 'N/A'),
                        'home_logo': fixture['teams']['home']['logo'],
                        'away_logo': fixture['teams']['away']['logo'],
                        'result': f"{fixture['goals']['home']} - {fixture['goals']['away']}"
                    })

    context = {
        'favorite_teams': favorite_teams,
        'fixtures': fixtures[:4],  
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

import requests
from datetime import datetime, timedelta
from collections import defaultdict
from django.shortcuts import render

def fetch_irish_premier_fixtures():
    url = f"https://{API_HOST}/fixtures"
    params = {
        'league': 357,  
        'season': 2024  
    }
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

def fixtures(request):
    fixture_response = fetch_irish_premier_fixtures()
    fixtures = fixture_response.get('response', [])

    current_date = datetime.utcnow().date()
    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    this_week_fixtures = []
    fixtures_by_round = defaultdict(list)

    for fixture in fixtures:
        fixture_date_str = fixture['fixture']['date']
        fixture_date = datetime.strptime(fixture_date_str[:10], '%Y-%m-%d').date()
        formatted_date = datetime.strptime(fixture_date_str, '%Y-%m-%dT%H:%M:%S%z').strftime('%d/%m/%Y %H:%M')

        
        venue = fixture.get('venue', {})
        venue_name = venue.get('name', 'Venue TBD')
        venue_city = venue.get('city', '')

        
        fixture_data = {
            'home_team': fixture['teams']['home']['name'],
            'away_team': fixture['teams']['away']['name'],
            'date': formatted_date,
            'venue': f"{venue_name}, {venue_city}" if venue_city else venue_name,
            'referee': fixture['fixture'].get('referee', 'Referee TBD'),
            'result': f"{fixture['goals']['home']} - {fixture['goals']['away']}",
            'home_logo': fixture['teams']['home'].get('logo', ''),
            'away_logo': fixture['teams']['away'].get('logo', '')
        }

        
        if start_of_week <= fixture_date <= end_of_week:
            this_week_fixtures.append(fixture_data)

        
        round_name = fixture['league']['round']
        fixtures_by_round[round_name].append(fixture_data)

    context = {
        'this_week_fixtures': this_week_fixtures,
        'fixtures_by_round': dict(fixtures_by_round)
    }
    
    return render(request, 'fixtures.html', context)

def fetch_nearby_places(query, types):
    results = {}

    if not settings.GOOGLE_API_KEY or settings.GOOGLE_API_KEY == 'your-google-api-key-here':
        
        return None, "Google API key is missing. Please provide your API key in settings.py."

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

    return results, None

def nearby_places(request, venue_name):
    types = ['restaurant', 'cafe', 'hotel', 'pub', 'parking', 'pharmacy', 'atm']
    places, error_message = fetch_nearby_places(venue_name, types)

    context = {
        'venue_name': venue_name,
        'places': places,
    }

    if error_message:
        context['error'] = error_message

    return render(request, 'nearby_places.html', context)

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

    
    favorite_team_ids = []
    if request.user.is_authenticated:
        favorite_team_ids = UserFavoriteTeam.objects.filter(user=request.user).values_list('team__id', flat=True)

    context = {
        'teams': teams,
        'favorite_team_ids': favorite_team_ids, 
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

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StadiumReview, Venue
from .forms import StadiumReviewForm
import requests


@login_required
def add_stadium_review(request, venue_id):
    try:
        venue = Venue.objects.get(id=venue_id)
    except Venue.DoesNotExist:
        # Fetch venue details from the API
        api_url = f"https://{API_HOST}/venues?id={venue_id}"
        response = requests.get(api_url, headers=HEADERS)
        
        if response.status_code == 200:
            venue_data = response.json().get('response', [])[0]
            venue = Venue.objects.create(
                id=venue_data['id'],
                name=venue_data['name'],
                address=venue_data.get('address', ''),
                city=venue_data.get('city', ''),
                capacity=venue_data.get('capacity', 0),
                image=venue_data.get('image', '')
            )
        else:
            messages.error(request, "Venue could not be found.")
            return redirect('home')
    
    reviews = venue.stadiumreview_set.all()

    if request.method == "POST":
        form = StadiumReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.venue = venue
            review.save()
            messages.success(request, "Your review has been added.")
            return redirect('add_stadium_review', venue_id=venue.id)
    else:
        form = StadiumReviewForm()

    return render(request, 'add_stadium_review.html', {'form': form, 'venue': venue, 'reviews': reviews})

@login_required
def venue_detail(request, venue_id):
    try:
        venue = Venue.objects.get(id=venue_id)
    except Venue.DoesNotExist:
        
        api_url = f"https://{API_HOST}/venues?id={venue_id}"
        response = requests.get(api_url, headers=HEADERS)
        
        if response.status_code == 200:
            venue_data = response.json().get('response', [])[0]
            venue = Venue.objects.create(
                id=venue_data['id'],
                name=venue_data['name'],
                address=venue_data.get('address', ''),
                city=venue_data.get('city', ''),
                capacity=venue_data.get('capacity', 0),
                image=venue_data.get('image', '')
            )
            
            return redirect('add_stadium_review', venue_id=venue.id)
        else:
            return render(request, '404.html', status=404)  
    else:
        
        reviews = StadiumReview.objects.filter(venue=venue)
        if not reviews.exists():
            return redirect('add_stadium_review', venue_id=venue.id)
    
    return render(request, 'venue_detail.html', {
        'venue': venue,
        'reviews': reviews,
    })

def fetch_standings(league_id, season):
    url = f"https://{API_HOST}/standings"
    params = {'league': league_id, 'season': season}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

def standings(request):
    league_id = 357  
    season = 2024    
    standings_data = fetch_standings(league_id, season)
    
    
    standings = standings_data.get('response', [])[0].get('league', {}).get('standings', [])[0] if standings_data['results'] > 0 else []

    context = {
        'standings': standings
    }
    return render(request, 'standings.html', context)


