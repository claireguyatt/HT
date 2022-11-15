from django.contrib import admin

from .forms import VariableForm, CategoricalVariableForm

# Register your models here.

admin.site.register(VariableForm)
admin.site.register(CategoricalVariableForm)
