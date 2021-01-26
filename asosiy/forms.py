from django.forms import ModelForm
from .models import NamozVaqti

class NamozVaqtiForm(ModelForm):
    class Meta:
        model = NamozVaqti
        fields = '__all__'
