from django.urls import path

from . import views

app_name = 'workshops'
urlpatterns = [
    path('', views.WorkshopList.as_view(), name='workshop-list'),
    path('register/', views.ParticipantCreate.as_view(), name='workshop-registration'),
    path('register/success/', views.ParticipantCreateSuccess.as_view(), name='workshop-registration-success')
]