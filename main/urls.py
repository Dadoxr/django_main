from django.urls import path
from main.apps import MainConfig
from main.views import MainPageView


app_name = MainConfig.name

urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
]