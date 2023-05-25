# django imports
from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User

# libary imports
import pandas as pd
from datetime import datetime

# project imports
from edit_variables.models import Variable
from .forms import GENDER_CHOICES, validate_date
from homepage.data_analysis.analyze_happiness import Happiness_Analyzer

# date validation for multiple delete
def validate_dates(start_date, end_date):
    if start_date >= end_date:
        raise ValidationError("Start date must preceed end date.")

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
    analysis = models.TextField()

    objects = ProfileManager()

    # return human-readable string for each object
    def __str__(self):
        return (self.username)

    # return URL for inidvidual model records
    def get_absolute_url(self):
        return 'model-detail-view', [str(self.id)]
    
    def get_categorical(self):
        return self.variables.all().filter(is_continuous=False)
    
    def get_continuous(self):
        return self.variables.all().filter(is_continuous=True)

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
            df = pd.concat([old_data, new_df])
            #df = old_data.concat(new_df)
            #df = old_data.append(new_df)

            # make sure data is sorted by date (incase old date was input)
            df = df.sort_index()

            # keep happiness at the end
            happiness_col = df.pop("Happiness")
            df["Happiness"] = happiness_col
            df = df.fillna(" ")
            self.data = df.to_dict(orient='split')
            
        # update analysis and save
        self.save()
        #if df.shape[0] > 1:
            #self.analyze()
        
    
    # user delete data
    def delete_data(self, date: str):

        # delete all data if no specific day
        if date == "all":
            self.data = dict()
        else:
            data = self.get_data()
            data = data.drop(date)
            self.data = data.to_dict(orient='split')
        self.save()

        #if self.data:
            #self.analyze()

    def delete_data_from_range(self, start_date, end_date):
        data = self.get_data()
        data = data.loc[(data.index < start_date) | (data.index > end_date)]
        self.data = data.to_dict(orient='split')

        self.save()
        # self.analyze()

    def download_data(self) -> None:

        data = self.get_data()
        date_time_str = datetime.today().strftime("%Y-%m-%d")
        data.to_csv('happiness_data' + date_time_str + '.csv')

    def analyze(self) -> None:
            
        analyzer = Happiness_Analyzer(self.get_data())
        analyzer.preprocess()
        analysis = analyzer.linear_reg()
        self.analysis = analysis
        self.save()
