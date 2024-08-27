from django import forms
from .models import FavoriteTeam

class FavoriteTeamForm(forms.ModelForm):
    class Meta:
        model = FavoriteTeam
        fields = ['team_name']
