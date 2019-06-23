import csv
import os
import django
from django.core.exceptions import ValidationError
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appday.settings')
django.setup()

from myapp.models import*
def load_data_into_table():
    fields = []
    with open("matches.csv", 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = csvreader.__next__()

        for team in csvreader:
            try:
                if(len(team)!=0):
                    bool_var = False
                    if team[9] == '0':
                        bool_var = False
                    else:
                        bool_var = True
                    m = Match(match_id = int(team[0]),season = int(team[1]),city = team[2],date = team[3],team1 = team[4],team2 = team[5],
                            toss_winner = team[6],toss_decision = team[7],match_result = team[8],dl_applied = bool_var,
                            winner = team[10],win_by_run = int(team[11]),win_by_wicket = int(team[12]),player_of_match = team[13],
                            venue = team[14],umpire1 = team[15],umpire2 = team[16],umpire3 = team[17])
                    m.save()
            except ValidationError:
                bool_var = False
                if team[9] == '0':
                    bool_var = False
                else:
                    bool_var = True
                a = team[3].split('/')
                year = '20' + a[2]
                month = a[1]
                day = a[0]
                temp = []
                temp.append(year)
                temp.append(month)
                temp.append(day)
                date_var = "-".join(temp)
                m = Match(match_id=int(team[0]), season=int(team[1]), city=team[2], date=date_var, team1=team[4], team2=team[5],
                          toss_winner=team[6], toss_decision=team[7], match_result=team[8], dl_applied=bool_var,
                          winner=team[10], win_by_run=int(team[11]), win_by_wicket=int(team[12]), player_of_match=team[13],
                          venue=team[14], umpire1=team[15], umpire2=team[16], umpire3=team[17])
                m.save()

def load_data_ball():
    fields = []
    with open("deliveries.csv", 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = csvreader.__next__()

        for eachball in csvreader:
            if(len(eachball)!=0):
                d = Balls(match_id = int(eachball[0]),innings = int(eachball[1]),batting_team = eachball[2],bowling_team = eachball[3],
                          over = int(eachball[4]),ball = int(eachball[5]),batsman = eachball[6],non_striker = eachball[7],bowler = eachball[8],
                          is_super_over = int(eachball[9]),wide_run = int(eachball[10]),bye_run = int(eachball[11]),legbye_run=int(eachball[12]),
                          noball_run = int(eachball[13]),penality_run = int(eachball[14]),batsman_run=int(eachball[15]),extra_run=int(eachball[16]),
                          total_run=int(eachball[17]),player_dismissed=eachball[18],dismissal_kind = eachball[19],fielder=eachball[20])
                d.matchh_id = Match.objects.get(match_id = int(eachball[0]))
                d.save()
if __name__ == '__main__':
    load_data_ball()
