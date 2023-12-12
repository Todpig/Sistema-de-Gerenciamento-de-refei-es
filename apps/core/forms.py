from django import forms 
from apps.core.models import Snack, RequestSnack

class RequestSnackForm(forms.ModelForm):
    class Meta:
        model = RequestSnack
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RequestSnackForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False

class SnackCreateForm(forms.ModelForm):
    class Meta:
        model = Snack
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SnackCreateForm, self).__init__(*args, **kwargs)
        self.fields['likes'].required = False
        self.fields['snack_to_day'].required = False
        self.fields['active'].required = False