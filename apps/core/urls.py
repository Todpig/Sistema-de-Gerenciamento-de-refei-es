from django.urls import path
from .views import *

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("today-menu", TodayMenu.as_view(), name="todayMenu"),
]
