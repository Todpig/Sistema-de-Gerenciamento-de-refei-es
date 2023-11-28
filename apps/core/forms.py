from django import forms 
from apps.core.models import Snack, RequestSnack

class RequestSnackForm(forms.ModelForm):
    class Meta:
        model = RequestSnack
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RequestSnackForm, self).__init__(*args, **kwargs)
        self.fields['student_name'].required = False
        self.fields['student_registration'].required = False