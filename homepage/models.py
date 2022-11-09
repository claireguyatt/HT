from tokenize import String
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

# models

class Variable(models.Model):
    name = models.CharField(max_length=100)
    prompt = models.CharField(max_length=250)

    # return human-readable string for each object
    def __str__(self):
        return self.name

    # return URL dor inidvidual model records
    # django automatically gives each object an id (primary key)
    def get_absolute_url(self):
        return 'model-detail-view', [str(self.id)]

# subclass of variable model
class Categorical_Variable(Variable):
    
    # if binary, choices are automatically Y/N
    is_binary = models.BooleanField()
    choices = models.JSONField()

GENDER_CHOICES = (
    ("Female", "Female"),
    ("Male", "Male"),
    ("Nonbinary", "Nonbinary"),
    ("Other", "Other")
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=20, help_text='Enter your username here')
    email = models.EmailField(max_length=254, help_text='Enter your email here')
    number = models.CharField(max_length=11, help_text='Enter your phone number here')
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Female')
    dob = models.DateField()
    variables = models.ManyToManyField(Variable)

    # return human-readable string for each object
    def __str__(self):
        return (self.username)

    # return URL dor inidvidual model records
    def get_absolute_url(self):
        return 'model-detail-view', [str(self.id)]



