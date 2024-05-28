# tabela/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, Match, Standings
from .forms import TeamForm, MatchForm, ResultForm

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
    matches = Match.objects.all()  # Modificação aqui
    return render(request, 'tabela/standings.html', {'standings': standings, 'matches': matches})

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
