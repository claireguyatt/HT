from django import forms
from django.forms import ModelForm
from homepage.models import Variable, CategoricalVariable
from django.utils.translation import gettext_lazy as _

class VariableForm(ModelForm):

    class Meta:
        model = Variable
        fields = ["name", "prompt",]

class CategoricalVariableForm(ModelForm):

    class Meta:
        model = CategoricalVariable
        fields = ["name", "prompt", "choices"]
        labels = {
            'choices': _('Variable response option'),
        }

