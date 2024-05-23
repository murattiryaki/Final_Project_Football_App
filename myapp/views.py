from django.shortcuts import render
import requests
import time
from datetime import datetime, timedelta
from collections import defaultdict
import urllib
from django.conf import settings

API_KEY = '0a1f33042a81c173f168fad17044385f'
API_HOST = 'v3.football.api-sports.io'
HEADERS = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': API_HOST
}

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

def home(request):
    return render(request, 'home.html')

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

from django.conf import settings

import logging

logger = logging.getLogger(__name__)

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

    context = {
        'teams': teams
    }
    return render(request, 'teams.html', context)




