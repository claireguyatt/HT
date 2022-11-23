from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Variable, CategoricalVariable

class VariableForm(ModelForm):

    class Meta:
        model = Variable
        fields = ["name", "prompt",]

class CategoricalVariableForm(ModelForm):

    class Meta:
        model = CategoricalVariable
        fields = ["name", "prompt", "choices",]
        labels = {
            'choices': _('Variable response option'),
        }

