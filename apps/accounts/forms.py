from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import *

GENDER =(
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other')
    )

class register_form(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,
                                 required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control text-secondary',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control text-secondary',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               error_messages={'required': 'Please enter Username'},
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control text-secondary',
                                                             }))
    email = forms.EmailField(required=True,
                             error_messages={'required': 'Please enter Email'},
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control text-secondary',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                error_messages={'required': 'Please enter password'},
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control text-secondary',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                error_messages={'required': 'Please enter confirm password'},
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control text-secondary',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class customAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               error_messages={'required': 'Please enter Username or Email!'},
                               widget=forms.TextInput(attrs={'placeholder': 'Your Username',
                                                             'class': 'form-control text-secondary',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               error_messages={'required': 'Please enter Password!'},
                               widget=forms.PasswordInput(attrs={'placeholder': 'Your Password',
                                                                 'class': 'form-control text-secondary',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    class Meta:
        fields = ['username', 'password', 'remember_me']

class updateUser_form(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               disabled=True,
                               widget=forms.TextInput(attrs={'class': 'form-control disabled'}))
    first_name = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100,
                               required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class updateProfile_form(forms.ModelForm):
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control','type':'file'}))
    headline = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    bio = forms.CharField(required=False,widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    gender = forms.ChoiceField(choices=GENDER, widget=forms.Select(attrs={'class': 'form-control'}))
      
    class Meta:
        model = Profile
        fields = ['profile_picture', 'gender', 'headline', 'bio']
