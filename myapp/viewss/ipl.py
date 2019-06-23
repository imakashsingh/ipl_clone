from django.views import View
from django.views.generic.edit import FormView
from myapp.models import *
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import *
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from myapp.forms.iplforms import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class SeasonView(View):
    def get(self,request,*args,**kwargs):
        if kwargs:
            matches = Match.objects.values('match_id','season','team1', 'team2', 'venue', 'toss_winner', 'toss_decision', 'winner',
                                           'player_of_match').filter(season= kwargs.get('season'))
        else:
            matches = Match.objects.values('match_id','season','team1', 'team2', 'venue', 'toss_winner', 'toss_decision', 'winner',
                                           'player_of_match').filter(season='2019')
        return render(request,
                      template_name="myapp/seasons_list.html",
                      context={
                          'title' : 'Matches in season {}'.format(matches[0]['season']),
                          'matches' : matches,
                          'list' : ['2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019']
                      })

class MatchView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request,*args,**kwargs):
        if kwargs['mid']:
            mid = kwargs['mid']
            matches = Match.objects.values('match_id','season','team1','team2','toss_winner','toss_decision','winner','win_by_run','win_by_wicket',
                                           'player_of_match').filter(match_id = kwargs['mid'])
            top_bowler1 = Balls.objects.filter(~Q(player_dismissed = ""),match_id=mid,innings = 1)
            top_bowler1 = top_bowler1.values('bowler').annotate(c= Count('player_dismissed')).order_by('-c')[:3]
            top_bowler2 = Balls.objects.filter(~Q(player_dismissed=""), match_id=mid, innings=2)
            top_bowler2 = top_bowler2.values('bowler').annotate(c=Count('player_dismissed')).order_by('-c')[:3]
            extra_runs  = Balls.objects.filter(match_id = mid)
            extra_runs = extra_runs.values('innings').annotate(s=Sum('extra_run'))
            top_batsman1 = Balls.objects.filter(match_id=mid, innings=1)
            top_batsman1 = top_batsman1.values('batsman').annotate(s=Sum('batsman_run')).order_by('-s')[:3]
            top_batsman2 = Balls.objects.filter(match_id=mid, innings=2)
            top_batsman2 = top_batsman2.values('batsman').annotate(s=Sum('batsman_run')).order_by('-s')[:3]
            teams = Balls.objects.values('batting_team','bowling_team').filter(match_id = mid,innings = 1).distinct()
            return render(request,
                          template_name="myapp/match_detail.html",
                          context={
                              'team1' : matches[0]['team1'],
                              'team2' : matches[0]['team2'],
                              'season' : matches[0]['season'],
                              'user': request.user,
                              'inn1' : '1',
                              'inn2' : '2',
                              'match_id' : matches[0]['match_id'],
                              'match_det' : matches,
                              'top_batsman1' : top_batsman1,
                              'top_batsman2': top_batsman2,
                              'extra1' : extra_runs[0]['s'],
                              'extra2': extra_runs[1]['s'],
                              'top_bowler1' : top_bowler1,
                              'top_bowler2' : top_bowler2,
                              'first_bat' : teams[0]['batting_team'],
                              'first_bowl' : teams[0]['bowling_team'],
                          })

class InningsView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request,*args,**kwargs):
        mid = kwargs['mid']
        inn = kwargs['inn']
        if inn == 1:
            match_det = Match.objects.values('team1','team2','season').get(match_id = kwargs['mid'])
            match_obj = Balls.objects.all().filter(match_id = mid,innings=1)
            return render(request,
                          template_name="myapp/inn_details.html",
                          context={
                              'team1' : match_det['team1'],
                              'team2' : match_det['team2'],
                              'user': request.user,
                              'season' : match_det['season'],
                              'inn_no' : 1,
                              'inn':match_obj,
                          })
        elif inn == 2:
            match_det = Match.objects.values('team1', 'team2', 'season').get(match_id=kwargs['mid'])
            match_obj = Balls.objects.all().filter(match_id=mid,innings=2)
            return render(request,
                          template_name="myapp/inn_details.html",
                          context={
                              'team1': match_det['team1'],
                              'team2': match_det['team2'],
                              'user': request.user,
                              'season': match_det['season'],
                              'inn_no': 2,
                              'inn': match_obj,
                          })

class PointsView(View):
    def get(self,request,*args,**kwargs):
        if kwargs:
            season = kwargs['season']
            t = Match.objects.values('team1', 'team2').filter(season=kwargs['season'], match_result="no result")
            m = Match.objects.filter(~Q(winner = ""),season=kwargs['season'])
        else:
            season = 2019
            t = Match.objects.values('team1', 'team2').filter(season = 2019, match_result="no result")
            m = Match.objects.filter(~Q(winner = ""),season=2019)
        m = m.values('winner').annotate(c=Count('winner')).order_by('-c')
        team_list = []
        temp_dict = {}
        no_matches_each = (len(m) - 1) * 2
        for team in m:
            temp_var = {}
            temp_dict[team['winner']] = (team['c'])*2
            temp_var['team'] = team['winner']
            temp_var['wins'] = (team['c'])
            temp_var['points'] = (team['c']) * 2
            temp_var['loses'] = ((no_matches_each) - team['c'])
            temp_var['tie'] = 0
            team_list.append(temp_var)
        for tie in t:
            team_name = tie['team1']
            for i in team_list:
                if team_name == i['team']:
                    i['points'] += 1
                    i['tie'] +=1
                    break
            team_name = tie['team2']
            for i in team_list:
                if team_name == i['team']:
                    i['points'] += 1
                    i['tie'] += 1
                    break

        return render(request,template_name="myapp/points_table.html",
                      context={
                          'title' : 'IPL {} Points Table'.format(season),
                          'teams' : team_list,
                          'tot_matches_each' : no_matches_each,
                          'list': ['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017',
                                   '2018', '2019']
                      })


class  LoginView(FormView):
    def get(self, request, *args, **kwargs):
        form = Login_form()
        return render(request,
                      template_name="myapp/logintemp.html",context={'form' : form})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = AuthenticationForm(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username = username,password = password)
            if user is not None:
                login(request,user)
                return redirect('defaul_matches_season')
            else:
                messages.error(request, 'username or password not correct')
                return redirect('login')
        else:
            form = AuthenticationForm()
            return render(request, 'myapp/logintemp.html', {'form': form})

class SignupView(FormView):
    def get(self, request, *args, **kwargs):
        form = SignUp_form()
        return render(request,
                      template_name='myapp/signup.html',context={'form':form})

    def post(self, request, *args, **kwargs):
        form = SignUp_form(request.POST)
        if form.is_valid():
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.create_user(username,password = password)
            user.save()
            if user is not None:
                login(request,user)
                return redirect('defaul_matches_season')
            else:
                return redirect('signup')


@login_required
def logout_func(request):
    logout(request)
    return redirect('defaul_matches_season')