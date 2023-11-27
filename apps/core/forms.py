from django import forms 
from apps.core.models import Snack, RequestSnack

class RequestSnackForm(forms.ModelForm):
    class Meta:
        model = RequestSnack
        fields = '__all__'