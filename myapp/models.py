from django.db import models

# Create your models here.

class Match(models.Model):
    match_id = models.IntegerField()
    season = models.IntegerField()
    city = models.CharField(max_length=128,null=True,blank=True)
    date = models.DateField()
    team1 = models.CharField(max_length=128)
    team2 = models.CharField(max_length=128)
    toss_winner = models.CharField(max_length=128,null=True,blank=True)
    toss_decision = models.CharField(max_length=128,null=True,blank=True)
    match_result = models.CharField(max_length=128,null=True,blank=True)
    dl_applied = models.BooleanField()
    winner = models.CharField(max_length=128,null=True,blank=True)
    win_by_run = models.IntegerField()
    win_by_wicket = models.IntegerField()
    player_of_match = models.CharField(max_length=128,null=True,blank=True)
    venue = models.CharField(max_length=128)
    umpire1 = models.CharField(max_length=128,null=True,blank=True)
    umpire2 = models.CharField(max_length=128,null=True,blank=True)
    umpire3 = models.CharField(max_length=128,null=True,blank=True)

    def __str__(self):
        return str(self.match_id)

class Balls(models.Model):
    match_id = models.IntegerField()
    innings = models.IntegerField()
    batting_team = models.CharField(max_length=128)
    bowling_team = models.CharField(max_length=128)
    over = models.IntegerField()
    ball = models.IntegerField()
    batsman = models.CharField(max_length=128)
    non_striker = models.CharField(max_length=128)
    bowler = models.CharField(max_length=128)
    is_super_over = models.IntegerField()
    wide_run = models.IntegerField()
    bye_run = models.IntegerField()
    legbye_run = models.IntegerField()
    noball_run = models.IntegerField()
    penality_run = models.IntegerField()
    batsman_run = models.IntegerField()
    extra_run = models.IntegerField()
    total_run = models.IntegerField()
    player_dismissed = models.CharField(max_length=128,null=True,blank=True)
    dismissal_kind = models.CharField(max_length=128,null=True,blank=True)
    fielder = models.CharField(max_length=128,null=True,blank=True)

    matchh_id = models.ForeignKey(Match,on_delete=models.CASCADE)

