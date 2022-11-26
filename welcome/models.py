from django.db import models

from django.contrib.auth.models import User
from edit_variables.models import Variable

import pandas as pd

# Profile model manager

class ProfileManager(models.Manager):
        
    def create_profile(self, user, username, email, number, gender, dob):

        profile = self.create(user=user, username=username, email=email, number=number, gender=gender, dob=dob)
        
        # add default variables
        default_vars = ["Sleep", "Temp", "Weather", "Happiness"]
        for var in default_vars:
            v = Variable.objects.get(name=var)
            profile.variables.add(v)
        
        return profile

# Profile model

GENDER_CHOICES = (
    ("Female", "Female"),
    ("Male", "Male"),
    ("Non binary", "Non binary"),
    ("Other", "Other")
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, help_text='Required. Enter your email.')
    number = models.CharField(max_length=11, help_text='Enter your phone number.')
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Female')
    dob = models.DateField()
    variables = models.ManyToManyField(Variable, related_name="users")
    data = models.JSONField(default=dict)

    objects = ProfileManager()

    # return human-readable string for each object
    def __str__(self):
        return (self.username)

    # return URL for inidvidual model records
    def get_absolute_url(self):
        return 'model-detail-view', [str(self.id)]
    
    def get_categorical(self):
        return self.variables.all().filter(is_continuous=False)

    # return user data in pd
    def get_data(self):

        # if no data return empty dataframe
        if (len(self.data) == 0):
            return pd.DataFrame()

        # otherwise return user's data
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
            # keep happiness at the end
            happiness_col = df.pop("Happiness")
            df["Happiness"] = happiness_col
            df = df.fillna(" ")
            self.data = df.set_index('date').to_dict(orient='split')

        # otherwise connvert previous data to dataframe & add new data
        else:
            new_df = pd.DataFrame(new_data, index=[0])
            new_df = new_df.set_index('date')
            df = old_data.append(new_df)

            # keep happiness at the end
            happiness_col = df.pop("Happiness")
            df["Happiness"] = happiness_col
            df = df.fillna(" ")

            self.data = df.to_dict(orient='split')
            print(self.data)
            
        # save profile data
        self.save()