from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Variable

class VariableForm(ModelForm):

    class Meta:
        model = Variable
        fields = ["name", "prompt",]
        labels = {
            'name': _('Variable name'),
            'prompt': _('Variable prompt')
        }

