# django imports
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.forms import ValidationError

# validation for continuous variable
def validate_scale(lower_bound:int, upper_bound:int):
    if lower_bound >= upper_bound:
        raise ValidationError("Lower bound must be lower than uppoer bound for conitnuous variable scale.")

# Variable model

class Variable(models.Model):
    name = models.CharField(max_length=30)
    prompt = models.CharField(max_length=250)
    is_continuous = models.BooleanField(default=False)

    # return human-readable string for each object
    def __str__(self):
        return self.name

    # return URL for inidvidual model records
    # django automatically gives each object an id (primary key)
    def get_absolute_url(self):
        return 'model-detail-view', [str(self.id)]

    # get categorical choices as a comma separated string
    def find_categorical_choices(self):
        cat_var = CategoricalVariable.objects.get(pk=self.pk)
        return cat_var.choices.split(",")
    # get categorical choices
    def get_choices(self):
        if self.is_cat_non_binary():
            return CategoricalVariable.objects.get(pk=self.pk).choices
        return None
    
    def is_cat_non_binary(self):
        if (CategoricalVariable.objects.filter(pk=self.pk).exists() and not CategoricalVariable.objects.get(pk=self.pk).is_binary):
            return True
        return False

    def get_upper(self):
        if self.is_continuous:
            return ContinuousVariable.objects.get(pk=self.pk).upper_bound
        return None
        
    def get_lower(self):
        if self.is_continuous:
            return ContinuousVariable.objects.get(pk=self.pk).lower_bound
        return None
    
    def check_delete(self):

        # delete from db if no longer attached to a user profile
        var = Variable.objects.get(id=self.id)
        safe_vars = ["Weather", "Happiness", "Temp", "Sleep"]
        is_safe = False
        for safe_var in safe_vars:
            if var.name == safe_var:
                is_safe = True
                break
        if is_safe == False:
            if not var.users.all():
                Variable.objects.get(id=self.id).delete()

# Variable model subclasses

class CategoricalVariable(Variable):
    
    # if binary, choices are automatically Y/N
    is_binary = models.BooleanField(default=True)
    choices = models.CharField(max_length=500)

class ContinuousVariable(Variable):
    lower_bound = models.IntegerField(default=0, help_text="Start of scale")
    upper_bound = models.IntegerField(default=10, help_text="End of scale")

