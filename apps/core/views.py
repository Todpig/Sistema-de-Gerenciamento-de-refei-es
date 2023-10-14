from django.shortcuts import render
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "index.html"

class TodayMenu(TemplateView):
    template_name = "todayMenu.html"