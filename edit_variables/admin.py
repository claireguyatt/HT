from django.contrib import admin

from .models import Variable, CategoricalVariable, ContinuousVariable

# Register your models here.

admin.site.register(Variable)
admin.site.register(CategoricalVariable)
admin.site.register(ContinuousVariable)
