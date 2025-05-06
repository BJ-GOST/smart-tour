from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import Textarea, TextInput, EmailInput, TextInput, PasswordInput, FileInput
from .models import User



class signUpForm(UserCreationForm):

    password1 = forms.CharField(
            widget = forms.PasswordInput(attrs={
            'style': 'height:100%; width:100%; border:1px solid #3f3cbb; border-radius:0.2rem; color:white; background:transparent; margin-top:15px; font-size:16px; padding: 1rem; font-family: "Roboto Mono", monospace;',
            'placeholder':'Password'
            })
    )

    password2 = forms.CharField(
            widget = forms.PasswordInput(attrs={
            'style': 'height:100%; width:100%; border:1px solid #3f3cbb;  border-radius:0.2rem; color:white; background:transparent; margin-top:15px; font-size:16px; padding: 1rem; font-family: "Roboto Mono", monospace;',
            'placeholder':'Confirm password'
            })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone_no']
        widgets={
            'username':TextInput(attrs={
                'style': 'height:100%; width:100%; border:1px solid #3f3cbb; border-radius:0.2rem; color:white; background:transparent; margin-top:15px;font-size:16px; padding: 1rem; font-family: "Roboto Mono", monospace;',
                'placeholder':'Username'
                }),
            'email':EmailInput(attrs={
                'style': 'height:100%; width:100%; border:1px solid #3f3cbb; border-radius:0.2rem; color:white; background:transparent; margin-top:15px;font-size:16px; padding: 1rem; font-family: "Roboto Mono", monospace;',
                'placeholder':'Email'
                }),
            'phone_no':TextInput(attrs={
                'style': 'height:100%; width:100%; border:1px solid #3f3cbb; border-radius:0.2rem; color:white; background:transparent; margin-top:15px;font-size:16px; padding: 1rem; font-family: "Roboto Mono", monospace;',
                'placeholder':'Contact'
                }),
		}