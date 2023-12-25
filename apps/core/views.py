from datetime import datetime
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
        context["almoco"] = Snack.objects.filter(
            type="almoço", snack_to_day=True, active=True)
        context["janta"] = Snack.objects.filter(
            type="janta", snack_to_day=True, active=True)
        return context


@method_decorator(login_required, name='dispatch')
class MyRequestsView(ListView):
    model = RequestSnack
    template_name = "myRequests.html"

    def get_context_data(self, **kwargs):
        context = super(MyRequestsView, self).get_context_data(**kwargs)
        context["myRequests"] = RequestSnack.objects.filter(
            user=self.request.user).order_by('-data')
        return context


def update_like(request, pk):
    snack = Snack.objects.get(pk=pk)

    liked_snacks = request.COOKIES.get('liked_snacks', '')

    if f'{pk}' in liked_snacks:
        messages.error(request, 'Você já curtiu esta refeição')
        return redirect('todayMenu')

    snack.likes += 1
    snack.save()

    liked_snacks += f'{pk},'
    response = redirect('todayMenu')
    response.set_cookie('liked_snacks', liked_snacks)

    return response


@method_decorator(login_required, name='dispatch')
class RequestSnackView(TemplateView):
    template_name = 'request-snack.html'
    form_class = RequestSnackForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form.instance.user = request.user

        form.instance.status = "pendente"

        existing_request = RequestSnack.objects.filter(
            user=request.user,
            data=form.data['data'],
            type=form.data['type']
        )

        if existing_request.exists():
            messages.error(
                request, 'Você já fez uma solicitação para esta data, por favor escolha outra data.')
            return render(request, 'request-snack.html', {'form': form})
        elif form.is_valid():
            form.save()
            return redirect('my-requests')
        else:
            messages.error(
                request, 'Formulário inválido. Corrija os erros abaixo.')
            return render(request, 'request-snack.html', {'form': form})


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
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
            self.send_message(f'Create the snack {
                              snack.description}', snackType)
            return redirect('create-meal')
        else:
            return self.render_to_response({'form': form})


@method_decorator(login_required, name='dispatch')
class SelectDishView(ListView):
    model = Snack
    template_name = "select-dish.html"

    def get_context_data(self, **kwargs):
        context = super(SelectDishView, self).get_context_data(**kwargs)
        context["almocos"] = Snack.objects.filter(
            active=True, type="almoço").order_by("?")
        context["jantares"] = Snack.objects.filter(
            active=True, type="janta").order_by("?")
        return context


def LogoutView(request):
    logout(request)
    return redirect('index')


@login_required
def approveRequestView(request, pk):
    snack_request = RequestSnack.objects.get(pk=pk)
    snack_request.status = "aprovado"
    snack_request.checked = True
    snack_request.save()

    send_approval_email(snack_request.user.email,
                        snack_request.data, snack_request.type)

    return redirect('all-request-meal')


@login_required
def rejectRequestView(request, pk):
    snack_request = RequestSnack.objects.get(pk=pk)
    snack_request.status = "reprovado"
    snack_request.checked = True
    snack_request.save()

    send_rejection_email(snack_request.user.email,
                         snack_request.data, snack_request.type)

    return redirect('all-request-meal')


@login_required
def selectSnackToDayView(request, pk):
    snack = Snack.objects.get(pk=pk)
    snackToDay = Snack.objects.filter(snack_to_day=True, type=snack.type)
    if snackToDay:
        messages.error(
            request, 'Já existe uma refeição selecionada para hoje, por favor desmarque a refeição selecionada para poder selecionar outra.')
        return redirect('select-dish')
    else:
        snack.snack_to_day = True
        snack.save()
        return redirect('select-dish')


@login_required
def removeSnackToDayView(request, pk):
    snack = Snack.objects.get(pk=pk)
    snack.snack_to_day = False
    snack.save()
    return redirect('select-dish')
