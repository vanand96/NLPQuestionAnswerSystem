from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('answer', views.answer, name='answer'),
    path('selected_house', views.selected_house, name='selected_house')
]
