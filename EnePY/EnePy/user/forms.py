from django import forms

from teaching.models import *
from user.models import *


class ChoiceControlWorkForm(forms.Form):
    number_kr = forms.ModelChoiceField(queryset=ControlWorks.objects.all(), empty_label='Выбирите кр', required=False)


class ChoiceGroupForm(forms.Form):
    number_group = forms.ModelChoiceField(queryset=Groups.objects.all(), empty_label='Выберите группу', required=False)

