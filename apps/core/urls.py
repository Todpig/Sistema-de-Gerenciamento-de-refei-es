from django.urls import path
from .views import *

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("meal/today-menu", TodayMenu.as_view(), name="todayMenu"),
    path("meal/request-snack", request_snack_view, name="request-snack"),
    path("meal/all-request-meal", AllRequestMealView.as_view(), name="all-request-meal"),
    path("create-meal", FormToCreateMealView.as_view(), name="create-meal"),
    path("meal/select-dish", SelectDishView.as_view(), name="select-dish"),
    path("logout/", LogoutView, name="logout"),
    path("meal/update-like/<int:pk>", update_like, name="update-like")
]