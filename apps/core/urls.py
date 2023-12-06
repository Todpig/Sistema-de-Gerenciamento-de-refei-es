from django.urls import path
from .views import *

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("meal/today-menu", TodayMenu.as_view(), name="todayMenu"),
    path("meal/request-snack", request_snack_view, name="request-snack"),
    path("meal/all-request-meal", AllRequestMealView.as_view(), name="all-request-meal"),
    path("meal/create-meal", FormToCreateMealView.as_view(), name="create-meal"),
    path("meal/select-dish", SelectDishView.as_view(), name="select-dish"),
    path("logout/", LogoutView, name="logout"),
    path("meal/update-like/<int:pk>", update_like, name="update-like"),
    path("approve-snack/<int:pk>", approveRequestView, name="approve-snack"),
    path("reject-snack/<int:pk>", rejectRequestView, name="reject-snack"),
    path("select-snack/<int:pk>", selectSnackToDayView, name="select-snack"),
    path("remove-snack/<int:pk>", removeSnackToDayView, name="remove-snack"),
]