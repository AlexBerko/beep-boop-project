from django import forms
from .models import *

class HelpForm(forms.ModelForm):
    class Meta:
        model = Help
        fields = ['title', 'full_info', 'deadline_date']
        # model.org_info
