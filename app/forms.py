from django import forms
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

class UniqueEmailValidator(UniqueValidator):
    def filter_queryset(self, value, queryset):
        return queryset.filter(email=value)

class UniqueUsernameValidator(UniqueValidator):
    def filter_queryset(self, value, queryset):
        return queryset.filter(username=value)

class RegisrationForm(forms.Form):
    email = forms.EmailField(validators=[UniqueEmailValidator(queryset=User.objects.all())])
    username = forms.CharField(validators=[UniqueUsernameValidator(queryset=User.objects.all())])
    password = forms.CharField(widget=forms.PasswordInput)

class PromptForm(forms.Form):
    prompt = forms.CharField(widget=forms.Textarea)

