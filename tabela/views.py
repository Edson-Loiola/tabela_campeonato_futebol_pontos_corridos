# tabela/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, Match, Standings
from .forms import TeamForm, MatchForm, ResultForm
from django.db.models import Sum

def add_team_view(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            Standings.objects.create(team=team)
            return redirect('standings')
    else:
        form = TeamForm()
    return render(request, 'tabela/add_team.html', {'form': form})

def add_match_view(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('standings')
    else:
        form = MatchForm()
    return render(request, 'tabela/add_match.html', {'form': form})

def standings_view(request):
    standings = Standings.objects.order_by('-points', '-goal_difference', '-goals_for')
    matches = Match.objects.all() 

    # Calcular o time que marcou mais gols
    goals_by_team = Match.objects.filter(played=True).values('home_team__name').annotate(total_goals=Sum('home_score'))
    goals_by_team = goals_by_team.union(Match.objects.filter(played=True).values('away_team__name').annotate(total_goals=Sum('away_score')))   
    top_scorer = max(goals_by_team, key=lambda x: x['total_goals']) if goals_by_team else None   

    return render(request, 'tabela\standings.html', {'standings': standings, 'matches': matches, 'top_scorer': top_scorer}) 


def update_result_view(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if request.method == 'POST':
        form = ResultForm(request.POST, instance=match)
        if form.is_valid():
            match = form.save()
            Standings.objects.get(team=match.home_team).update_standings()
            Standings.objects.get(team=match.away_team).update_standings()
            return redirect('standings')
    else:
        form = ResultForm(instance=match)
    return render(request, 'tabela/update_result.html', {'form': form})

def reset_championship(request):
    # Excluir todas as entradas das tabelas de times e partidas
    Team.objects.all().delete()
    Match.objects.all().delete()
    # Redirecionar de volta para a página da tabela
    return redirect('standings')

def delete_match(request, match_id):
    match = Match.objects.get(pk=match_id)
    if match.played:
        home_team_standings = Standings.objects.get(team=match.home_team)
        away_team_standings = Standings.objects.get(team=match.away_team)

        home_team_standings.played -= 1
        away_team_standings.played -= 1

        if match.home_score > match.away_score:
            home_team_standings.points -= 3
            home_team_standings.won -= 1
            away_team_standings.lost -= 1
        elif match.home_score < match.away_score:
            away_team_standings.points -= 3
            away_team_standings.won -= 1
            home_team_standings.lost -= 1
        else:
            home_team_standings.points -= 1
            away_team_standings.points -= 1
            home_team_standings.drawn -= 1
            away_team_standings.drawn -= 1

        home_team_standings.goals_for -= match.home_score
        home_team_standings.goals_against -= match.away_score
        away_team_standings.goals_for -= match.away_score
        away_team_standings.goals_against -= match.home_score
        home_team_standings.goal_difference = home_team_standings.goals_for - home_team_standings.goals_against
        away_team_standings.goal_difference = away_team_standings.goals_for - away_team_standings.goals_against

        home_team_standings.save()
        away_team_standings.save()

    match.delete()
    return redirect('standings') 
