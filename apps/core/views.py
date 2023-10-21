from django.shortcuts import render
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "index.html"

class TodayMenu(TemplateView):
    template_name = "todayMenu.html"

class RequestSnackView(TemplateView):
    template_name = "request-snack.html"

class RequestDinnerView(TemplateView):
    template_name = "request-dinner.html"

class AllRequestMealView(TemplateView):
    template_name = "allRequestMeal.html"

class FormToCreateMealView(TemplateView):
    template_name = "formToCreateMeal.html"