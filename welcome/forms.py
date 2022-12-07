from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import datetime

GENDER_CHOICES = (
    ("Woman", "Woman"),
    ("Man", "Man"),
    ("Non binary", "Non binary"),
    ("Other", "Other")
)

# Create your forms here.

def validate_date(input_date):
	if input_date > datetime.date.today():
		raise forms.ValidationError("DOB cannot be in the future. Unless you are a time traveller. Then you're probably smart enough to figure out how to bypass this validator.")

class NewUserForm(UserCreationForm):

	email = forms.EmailField(max_length=254, help_text='Enter your email here', required=True)
	number = forms.CharField(max_length=11, help_text='Enter your phone number here', required=False)
	dob = forms.DateField(required=True, help_text="Enter a date in the format mm/dd/yyyy", validators={validate_date})
	gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

	def clean(self):
		
		cd = self.cleaned_data

		input_username = cd.get("username")

		if User.objects.filter(username=input_username).exists():
			raise forms.ValidationError(f'Username {input_username} is already in use.')

		return cd
