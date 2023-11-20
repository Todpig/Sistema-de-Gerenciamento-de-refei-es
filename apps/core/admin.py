from django.contrib import admin
from apps.core.models import Snack, RequestSnack

@admin.register(Snack)
class SnackAdmin(admin.ModelAdmin):
    list_display = ("description", "likes", "snack_to_day", "type", "active")

@admin.register(RequestSnack)
class RequestSnackAdmin(admin.ModelAdmin):
    list_display = ("student_name", "student_registration", "data", "justification", "status", "type")
