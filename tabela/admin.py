# tabela/admin.py
from django.contrib import admin
from .models import Team, Match, Standings

admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Standings)
