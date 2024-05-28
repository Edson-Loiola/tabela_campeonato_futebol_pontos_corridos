# tabela/models.py
from django.db import models
from django.db.models import Sum, Q, F

class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    played = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.home_team} X {self.away_team}"

    @property
    def result(self):
        if self.played:
            return f"{self.home_score} - {self.away_score}"
        return "Partida Não Realizada"

class Standings(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    played = models.IntegerField(default=0)
    won = models.IntegerField(default=0)
    drawn = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    goal_difference = models.IntegerField(default=0)

    def __str__(self):
        return self.team.name

    def update_standings(self):
        matches = Match.objects.filter(Q(home_team=self.team) | Q(away_team=self.team), played=True)
        self.played = matches.count()

        self.won = matches.filter(
            Q(home_team=self.team, home_score__gt=F('away_score')) |
            Q(away_team=self.team, away_score__gt=F('home_score'))
        ).count()

        self.drawn = matches.filter(home_score=F('away_score')).count()

        self.lost = matches.filter(
            Q(home_team=self.team, home_score__lt=F('away_score')) |
            Q(away_team=self.team, away_score__lt=F('home_score'))
        ).count()

        goals_for_home = matches.filter(home_team=self.team).aggregate(total=Sum('home_score'))['total'] or 0
        goals_for_away = matches.filter(away_team=self.team).aggregate(total=Sum('away_score'))['total'] or 0
        self.goals_for = goals_for_home + goals_for_away

        goals_against_home = matches.filter(home_team=self.team).aggregate(total=Sum('away_score'))['total'] or 0
        goals_against_away = matches.filter(away_team=self.team).aggregate(total=Sum('home_score'))['total'] or 0
        self.goals_against = goals_against_home + goals_against_away

        self.goal_difference = self.goals_for - self.goals_against
        self.points = self.won * 3 + self.drawn

        self.save()
