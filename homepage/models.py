from tokenize import String
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

GENDER_CHOICES = (
    ("Female", "Female"),
    ("Male", "Male"),
    ("Nonbinary", "Nonbinary"),
    ("Other", "Other")
)

# abstract variable
class Variable(models.Model):
    name = models.CharField(max_length=100)
    prompt = models.CharField(max_length=250)
  
    class Meta:
        abstract = True
    
    def check_input():
        pass

# concrete variables
class Binary_Variable(Variable):

    def check_input(self):

        # allowed responses
        bools = ['Y', 'N']
        
        var_data = input(self.prompt + '\n')
        # only accept Y/N boolean response otherwise ask again
        while var_data not in bools:
            var_data = input(self.prompt + '\n')
        return var_data

class Categorical_Variable(Variable):
    
    def check_input(self):

        var_data = input(self.prompt + '\n')
        # only accept digit response otherwise ask again
        while var_data.isdigit()==False:
            var_data = input(self.prompt + '\n')
        return var_data

class Continuous_Variable(Variable):

    # can't have more than 12 choices
    choices = ArrayField(models.CharField(max_length=100), size=12)

    def check_input(self):

        var_data = input(self.prompt + '\n')
        # only accept choices from the list otherwise ask again
        while var_data not in self.choices:
            var_data = input(self.prompt + '\n')
        return var_data

class Profile(models.Model):
    username = models.CharField(max_length=20, verbose_name='First name', help_text='Enter your username here')
    email = models.EmailField(max_length=254, help_text='Enter your email here')
    number = models.CharField(max_length=11, help_text='Enter your phone number here')
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Female')
    dob = models.DateField()
    variables = models.ForeignKey(Variable)

    # return human-readable string for each object
    def __str__(self):
        return (self.fName + " " + self.lName)

    # return URL dor inidvidual model records
    # django automatically gives each object an id (primary key)
    def get_absolute_url(self):
        return 'model-detail-view', [str(self.id)]



