from django.urls import path
from .views import *

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("today-menu", TodayMenu.as_view(), name="todayMenu"),
    path("request-snack", RequestSnackView.as_view(), name="request-snack"),
    path("request-dinner", RequestDinnerView.as_view(), name="request-dinner"),
    path("all-request-meal", AllRequestMealView.as_view(), name="all-request-meal")
]
