from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Snack, RequestSnack
class IndexView(TemplateView):
    template_name = "index.html"

class TodayMenu(ListView):
    model = Snack
    template_name = "todayMenu.html"

    def get_context_data(self, **kwargs):
        context = super(TodayMenu, self).get_context_data(**kwargs)
        context["almoco"] = Snack.objects.filter(type="almoço", snack_to_day=True, active=True)
        context["janta"] = Snack.objects.filter(type="janta", snack_to_day=True, active=True)
        return context
class RequestSnackView(TemplateView):
    template_name = "request-snack.html"

class RequestDinnerView(TemplateView):
    template_name = "request-dinner.html"

class AllRequestMealView(ListView):
    model = RequestSnack
    template_name = "allRequestMeal.html"

    def get_context_data(self, **kwargs):
        context = super(AllRequestMealView, self).get_context_data(**kwargs)
        context["requests"] = RequestSnack.objects.all()
        context["qtd_requests"] = RequestSnack.objects.count()
        return context

class FormToCreateMealView(TemplateView):
    template_name = "formToCreateMeal.html"
class SelectDishView(ListView):
    model = Snack
    template_name = "select-dish.html"

    def get_context_data(self, **kwargs):
        context = super(SelectDishView, self).get_context_data(**kwargs)
        context["almocos"] = Snack.objects.filter(active=True, type="almoço")
        context["jantares"] = Snack.objects.filter(active=True, type="janta")
        return context