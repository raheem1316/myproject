from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User


from queriesapp.models import Profile


class SignupForm(forms.Form):
    first_name=forms.CharField(max_length=20)
    last_name=forms.CharField(max_length=20)
    email=forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget = forms.PasswordInput())

class LoginForm(forms.Form):
   email = forms.EmailField()
   password = forms.CharField(widget = forms.PasswordInput())

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name')

class ProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(widget=forms.RadioSelect,choices=Profile.GENDER,label='Gender')

    class Meta:
        model = Profile
        fields = ('gender','profile_pic')

class ChangepasswordForm(forms.Form):
    Old_password = forms.CharField(widget=forms.PasswordInput())
    New_password = forms.CharField(widget=forms.PasswordInput())
    Confirm_Newpassword = forms.CharField(widget=forms.PasswordInput())

class CommentsForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'write your answer here'}))
    upload_file=forms.FileField(required=False)
