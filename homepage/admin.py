from django.contrib import admin
from .models import Profile, Variable, Categorical_Variable

# Register your models here.

# original registration
#admin.site.register(Profile)

# admin class for model registration --> gives more options for display on mysql
class ProfileAdmin(admin.ModelAdmin):
    #list_display = ('fName', 'lName', )
    pass

# register admin class w associated model
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Variable)
admin.site.register(Categorical_Variable)
