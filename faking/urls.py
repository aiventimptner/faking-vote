from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path

urlpatterns = [
    path('', lambda request: render(request, 'faking/index.html')),
    path('votes/', include('votes.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
