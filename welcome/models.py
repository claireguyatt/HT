from django.db import models
from django.forms import ValidationError

from django.contrib.auth.models import User
from edit_variables.models import Variable

import pandas as pd
from datetime import datetime

from .forms import GENDER_CHOICES, validate_date

# Profile model manager

class ProfileManager(models.Manager):
        
    # new user
    def create_profile(self, user, username, email, number, gender, dob):

        profile = self.create(user=user, username=username, email=email, number=number, gender=gender, dob=dob)
        
        # add default variables
        default_vars = [1, 2, 3, 4]
        for var_key in default_vars:
            v = Variable.objects.get(pk=var_key)
            profile.variables.add(v)
        
        return profile
    
    # guest user for exploring site
    def create_guest_profile(self, user):
        
        # create profile without extra user info
        profile = self.create(user=user, username=user.username)

        # add default variables
        default_vars = ["Sleep", "Temp", "Weather", "Happiness"]
        for var in default_vars:
            v = Variable.objects.get(name=var)
            profile.variables.add(v)
        
        return profile

# Profile model

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, help_text='Required. Enter your email.', unique=True)
    number = models.CharField(max_length=11, help_text='Enter your phone number.')
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Woman')
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

        # otherwise convert previous data to dataframe & add new data
        else:

            new_df = pd.DataFrame(new_data, index=[0])

            new_date = new_df['date'].values[0]

            # validate date (can't be in the future, can't already be added)

            validate_date(datetime.strptime(new_date, '%Y-%m-%d').date())

            if (new_date in old_data.index):
                raise ValidationError(new_date + " has already been added. To re-add, first delete this day's data from the homepage.")

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
    
    # user delete data
    def delete_data(self, day: str):

        # delete all data if no specific day
        if day == "all":
            self.data = dict()
        else:
            data = self.get_data()
            data = data.drop(day)
            self.data = data.to_dict(orient='split')
        self.save()