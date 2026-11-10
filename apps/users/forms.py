from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Student

class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Student
        fields = ('username', 'email', 'student_number', 'campus')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@funaab.edu.ng'):
            raise forms.ValidationError("You must register with a valid @funaab.edu.ng email address.")
        return email

class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('username', 'email', 'student_number', 'campus')