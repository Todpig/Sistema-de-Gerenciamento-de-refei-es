from datetime import datetime
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView
from .models import Snack, RequestSnack
from apps.core.forms import RequestSnackForm
from django.contrib.auth import logout
from django.contrib import messages
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
    
def update_like(request, pk):
    snack = Snack.objects.get(pk=pk)
    snack.likes += 1
    snack.save()
    context = {}
    context["almoco"] = Snack.objects.filter(type="almoço", snack_to_day=True, active=True)
    context["janta"] = Snack.objects.filter(type="janta", snack_to_day=True, active=True)
    return render(request, "todayMenu.html", context)

def request_snack_view(request):
    if request.method == 'POST':
        form = RequestSnackForm(request.POST)
        form.instance.created_by = request.user

        try:
            form.instance.data = datetime.strptime(form.data['data'], '%d/%m/%Y').strftime('%Y-%m-%d')
        except ValueError:
            messages.error(request, 'Formato de data inválido. Use o formato DD/MM/AAAA.')
            return render(request, 'request-snack.html', {'form': form})

        existing_request = RequestSnack.objects.filter(
            student_registration=request.user.username,
            data=form.instance.data,
            type=form.data['type']
        )
        if existing_request.exists():
            messages.error(request, 'Você já fez uma solicitação para esta data, por favor escolha outra data.')
        elif form.is_valid():
            form.instance.student_name = request.user.first_name + " " + request.user.last_name
            form.instance.student_registration = request.user.username
            form.save()
            # messages.success(request, 'Solicitação enviada com sucesso.')
            return redirect('index')
        else:
            messages.error(request, 'Formulário inválido. Corrija os erros abaixo.')
            print(form.errors)
    else:
        form = RequestSnackForm()

    return render(request, 'request-snack.html', {'form': form})

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

def LogoutView(request):
    logout(request)
    return redirect('index')