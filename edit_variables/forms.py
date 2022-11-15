from django import forms
from django.forms import ModelForm
from homepage.models import Variable, Categorical_Variable
from django.core.exceptions import ValidationError

class VariableForm(ModelForm):

    class Meta:
        model = Variable
        fields = ["name", "prompt"]

        # this function will be used for the validation
    def clean(self):
    
        # data from the form is fetched using super function
        super(VariableForm, self).clean()
        
        # extract fields from data
        name = self.cleaned_data.get("name")
        text = self.cleaned_data.get("prompt")

        # conditions to be met for the name & prompt

        # can't be only spaces
        if not text.replace(" ", "").length() == 0:
            raise ValidationError({name: "Must include prompt"})

        # return any errors if found
        return self.cleaned_data

class CategoricalVariableForm(ModelForm):

    class Meta:
        model = Categorical_Variable
        fields = ["name", "prompt", "choices"]

