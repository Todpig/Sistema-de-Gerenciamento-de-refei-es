from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from .models import Snack, RequestSnack
from apps.core.forms import RequestSnackForm
from django.contrib.auth import logout
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
    
class RequestSnackView(CreateView):
    template_name = "request-snack.html"
    form_class = RequestSnackForm
    model = RequestSnack
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super(RequestSnackView, self).get_context_data(**kwargs)
        context['form'] = RequestSnackForm()  
        return context
class AllRequestMealView(ListView):
    model = RequestSnack
    template_name = "allRequestMeal.html"
    form_class = RequestSnackForm
    success_url = "/"

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

def logout_view(request):
    logout(request)