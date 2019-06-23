from django.urls import *
from myapp.viewss.ipl import *

urlpatterns = [
    path('iplapp/seasons',SeasonView.as_view(),name = "defaul_matches_season"),
    path('iplapp/seasons/<str:season>',SeasonView.as_view(),name = "param_matches_season"),
    path('iplapp/match/<int:mid>',MatchView.as_view(),name = "match_details"),
    path('iplapp/match/<int:mid>/<int:inn>',InningsView.as_view(),name = "innings_details"),
    path('login/',LoginView.as_view(),name = "login"),
    path('logout/',logout_func,name = "logout"),
    path('signup/',SignupView.as_view(),name = "signup"),
    path('iplapp/points',PointsView.as_view(),name = "points_default"),
    path('iplapp/points/<int:season>',PointsView.as_view(),name = "points"),
]