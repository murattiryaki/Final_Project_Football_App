# Football Match Day Travel Planning App
(https://murattiryaki.pythonanywhere.com/)

This is a web application that helps football fans organize their matchday travels. The app allows users to search for football teams, venues and fixtures, add favorite teams, leave stadium reviews, monitor league standings, get directions to stadiums and explore nearby points of interest (POIs) such as restaurants, hotels, pubs and more.

## Features
- Search football teams, venues and fixtures
- View nearby places around stadiums
- Add and manage favorite teams
- Leave reviews and ratings for stadiums
- Get directions to stadiums
- Explore nearby points of interest (POIs)

## Getting Started

### Prerequisites

- Python 3.9.6
- Django 4.2.16
- Google Places API key (optional, but required for the "Nearby Places" feature)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/murattiryaki/Final_Project_Football_App.git
   cd Final_Project_Football_App

2. **Create and activate a virtual environment (optional, but recommended):**

   On macOS/Linux:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

   On Windows:
   ```bash
   python -m venv env
   env\Scripts\activate
   ```


4. **Install the required dependencies:**
   
   pip3 install -r requirements.txt

5. **Google API Key (Optional):**

   Ask for Google Location API Key or provide one to replace GOOGLE_API_KEY = '' with GOOGLE_API_KEY = 'your-google-api-key-here' in settings.py
   If you do not provide the key, the "Nearby Places" feature will display a message indicating that the API key is required.

7. **Run the server:**
   
   python3 manage.py runserver


