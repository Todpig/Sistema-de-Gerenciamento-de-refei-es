from datetime import datetime
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView

from apps.core.sendEmail import send_approval_email, send_rejection_email
from .models import Snack, RequestSnack
from apps.core.forms import RequestSnackForm, SnackCreateForm
from django.contrib.auth import logout
from django.contrib import messages
from Gerenciamento_de_Refeicao.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_S3_REGION_NAME,
    AWS_SECRET_ACCESS_KEY,
    URL_SQS,
)
import boto3
import uuid

sqs = boto3.client(
    "sqs",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name="sa-east-1",
)
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
    return redirect('todayMenu')

def request_snack_view(request):
    if request.method == 'POST':
        form = RequestSnackForm(request.POST)
        form.instance.created_by = request.user
        form.instance.status = "pendente"
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
            form.instance.student_email = request.user.email
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
        unchecked_requests = RequestSnack.objects.filter(checked=False)    
        context["requests"] = unchecked_requests.order_by('-data')
        context["qtd_requests"] = unchecked_requests.count()
        
        return context


class FormToCreateMealView(TemplateView):
    template_name = "formToCreateMeal.html"
    form_class = SnackCreateForm

    def send_message(self, message_body, message_group_id):
        sqs.send_message(
            QueueUrl=URL_SQS,
            MessageBody=message_body,
            MessageGroupId=message_group_id,
            MessageDeduplicationId=str(uuid.uuid4())
        )

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            snack = form.save()
            snackType = snack.type
            if snackType == "almoço":
                snackType = "almoco"
            self.send_message(f'Create the snack {snack.description}', snackType)
            return redirect('create-meal')
        else:
            return self.render_to_response({'form': form})
   
    
class SelectDishView(ListView):
    model = Snack
    template_name = "select-dish.html"

    def get_context_data(self, **kwargs):
        context = super(SelectDishView, self).get_context_data(**kwargs)
        context["almocos"] = Snack.objects.filter(active=True, type="almoço").order_by("?")
        context["jantares"] = Snack.objects.filter(active=True, type="janta").order_by("?")
        return context

def LogoutView(request):
    logout(request)
    return redirect('index')

def approveRequestView(request, pk):
    snack_request = RequestSnack.objects.get(pk=pk)
    snack_request.status = "aprovado"
    snack_request.checked = True
    snack_request.save()

    send_approval_email(snack_request.student_email, snack_request.data, snack_request.type)

    return redirect('all-request-meal')

def rejectRequestView(request, pk):
    snack_request = RequestSnack.objects.get(pk=pk)
    snack_request.status = "reprovado"
    snack_request.checked = True
    snack_request.save()

    send_rejection_email(snack_request.student_email, snack_request.data, snack_request.type)

    return redirect('all-request-meal')

def selectSnackToDayView(request, pk):
    snack = Snack.objects.get(pk=pk)
    snack.snack_to_day = True
    snack.save()
    return redirect('select-dish')

def removeSnackToDayView(request, pk):
    snack = Snack.objects.get(pk=pk)
    snack.snack_to_day = False
    snack.save()
    return redirect('select-dish')