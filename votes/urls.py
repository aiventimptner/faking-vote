from django.urls import path

from . import views

app_name = 'votes'
urlpatterns = [
    path('', views.DecisionIndex.as_view(), name='index'),
    path('create/', views.DecisionCreate.as_view(), name='create'),
    path('<int:pk>/', views.DecisionInfo.as_view(), name='info'),
    path('<int:pk>/vote/', views.VoteCreate.as_view(), name='vote'),
]
