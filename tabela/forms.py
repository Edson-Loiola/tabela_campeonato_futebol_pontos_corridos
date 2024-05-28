# tabela/forms.py
from django import forms
from .models import Team, Match

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['home_team', 'away_team']

class ResultForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['home_score', 'away_score', 'played']
