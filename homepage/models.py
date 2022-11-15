from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_slug

import json
import pandas as pd

# models

class Variable(models.Model):
    name = models.CharField(max_length=100, validators=[validate_slug])
    prompt = models.CharField(max_length=250)
    is_continuous = models.BooleanField()

    # return human-readable string for each object
    def __str__(self):
        return self.name

    # return URL for inidvidual model records
    # django automatically gives each object an id (primary key)
    def get_absolute_url(self):
        return 'model-detail-view', [str(self.id)]

    def find_categorical_choices(self):
        cat_var = Categorical_Variable.objects.get(name=self.name)
        return cat_var.choices.split(",")

# subclass of variable model
class Categorical_Variable(Variable):
    
    # if binary, choices are automatically Y/N
    choices = models.CharField(max_length=500, help_text="enter your categories here (comma separated)")

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
    data = models.JSONField(default=dict)

    # return human-readable string for each object
    def __str__(self):
        return (self.username)

    # return URL for inidvidual model records
    def get_absolute_url(self):
        return 'model-detail-view', [str(self.id)]
    
    def get_categorical(self):
        return self.variables.all().filter(is_continuous=False)

    # add data to user profile from user input
    def add_day(self, user_input: dict):

        # remove useless info
        new_data = user_input.dict()
        new_data.pop("csrfmiddlewaretoken")
        new_data.pop("submit")

        # if previous data is empty, disregard
        if (len(self.data) == 0):
            df = pd.DataFrame(new_data, index=[0])
            self.data = df.set_index('date').to_dict(orient='split')
        # otherwise connvert previous data to dataframe & add new data
        else:
            # convert to df
            index = self.data.get('index')
            columns = self.data.get("columns")
            rows = self.data.get("data")
            df = pd.DataFrame(rows, index, columns)
            
            # append new data
            new_df = pd.DataFrame(new_data, index=[0])
            new_df = new_df.set_index('date')
            df = df.append(new_df)
            print(df)
            self.data = df.to_dict(orient='split')
            
        # save profile data
        self.save()
        


    

    

    



