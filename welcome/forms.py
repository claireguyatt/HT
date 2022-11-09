from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

GENDER_CHOICES = (
    ("Female", "Female"),
    ("Male", "Male"),
    ("Nonbinary", "Nonbinary"),
    ("Other", "Other")
)

class NewUserForm(UserCreationForm):

	email = forms.EmailField(max_length=254, help_text='Enter your email here', required=True)
	number = forms.CharField(max_length=11, help_text='Enter your phone number here', required=False)
	dob = forms.DateField(required=True)
	gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2", "dob")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.number = self.cleaned_data['number']
		user.dob = self.cleaned_data['dob']
		user.gender = self.cleaned_data['gender']
		if commit:
			user.save()
		return user