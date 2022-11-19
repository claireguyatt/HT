from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_slug
from django.core.exceptions import ValidationError

import pandas as pd

# models

class Variable(models.Model):
    name = models.CharField(max_length=30, unique=True)
    prompt = models.CharField(max_length=250)
    is_continuous = models.BooleanField(default=False)

    # return human-readable string for each object
    def __str__(self):
        return self.name

    # return URL for inidvidual model records
    # django automatically gives each object an id (primary key)
    def get_absolute_url(self):
        return 'model-detail-view', [str(self.id)]

    def find_categorical_choices(self):
        cat_var = CategoricalVariable.objects.get(name=self.name)
        return cat_var.choices.split(",")
    
    def is_cat_non_binary(self):
        if (CategoricalVariable.objects.filter(name=self.name).exists() and not CategoricalVariable.objects.get(name=self.name).is_binary):
            return True
        return False

    def get_choices(self):
        if self.is_cat_non_binary:
            return CategoricalVariable.objects.get(name=self.name).choices
        return None


# subclass of variable model
class CategoricalVariable(Variable):
    
    # if binary, choices are automatically Y/N
    is_binary = models.BooleanField(default=True)
    choices = models.CharField(max_length=500)

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
    variables = models.ManyToManyField(Variable, related_name="users")
    data = models.JSONField(default=dict)

    # return human-readable string for each object
    def __str__(self):
        return (self.username)

    # return URL for inidvidual model records
    def get_absolute_url(self):
        return 'model-detail-view', [str(self.id)]
    
    def get_categorical(self):
        return self.variables.all().filter(is_continuous=False)

    def get_data(self):

        # if no data return false
        if (len(self.data) == 0):
            return pd.DataFrame()

        # else convert user data to df & return
        #data_as_dict = json.loads(self.data)
        #index = data_as_dict.get('index')
        #columns = data_as_dict.get("columns")
        #rows = data_as_dict.get("data")

        index = self.data.get('index')
        columns = self.data.get("columns")
        rows = self.data.get("data")

        return pd.DataFrame(rows, index, columns)

    # add data to user profile from user input
    def add_day(self, user_input: dict):

        # remove useless info
        new_data = user_input.dict()
        new_data.pop("csrfmiddlewaretoken")
        new_data.pop("submit")

        old_data = self.get_data()

        # if previous data is empty, disregard
        if (old_data.empty):
            df = pd.DataFrame(new_data, index=[0])
            self.data = df.set_index('date').to_dict(orient='split')

        # otherwise connvert previous data to dataframe & add new data
        else:
            new_df = pd.DataFrame(new_data, index=[0])
            new_df = new_df.set_index('date')
            old_data = old_data.append(new_df)
            self.data = old_data.to_dict(orient='split')
            
        # save profile data
        self.save()
    
        
        


    

    

    



