from django import forms
from .models import *

class HelpForm(forms.ModelForm):
    class Meta:
        model = Help
        fields = ['title', 'full_info']
        # model.org_info
