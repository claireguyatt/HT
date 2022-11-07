from django.contrib import admin
from .models import Profile

# Register your models here.

# original registration
#admin.site.register(Profile)

# admin class for model registration --> gives more options for display on mysql
class ProfileAdmin(admin.ModelAdmin):
    #list_display = ('fName', 'lName', )
    pass

# register admin class w associated model
admin.site.register(Profile, ProfileAdmin)
