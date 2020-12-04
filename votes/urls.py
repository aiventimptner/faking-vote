from django.urls import path

from . import views

app_name = 'votes'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/result/', views.ResultsView.as_view(), name='results'),
    path('<int:decision_id>/vote/', views.vote, name='vote'),
]
