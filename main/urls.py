from django.urls import path
from django.views.decorators.cache import cache_page
from main.apps import MainConfig
from main.views import MainPageView


app_name = MainConfig.name

urlpatterns = [
    path('', cache_page(60)(MainPageView.as_view()), name='main'),
]