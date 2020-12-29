from django.urls import path

from . import views

app_name = 'votes'
urlpatterns = [
    path('', views.Decisions.as_view(), name='decisions'),
    path('create/', views.DecisionCreate.as_view(), name='create'),
    path('owned/', views.DecisionsOwned.as_view(), name='owned'),
    path('results/', views.DecisionResults.as_view(), name='results'),
    path('<int:pk>/', views.DecisionInfo.as_view(), name='info'),
    path('<int:pk>/result/', views.DecisionResult.as_view(), name='result'),
    path('<int:pk>/vote/', views.VoteCreate.as_view(), name='vote'),
]
