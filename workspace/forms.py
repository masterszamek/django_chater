from django import forms
from django.forms.widgets import PasswordInput


class HiddenWorkspaceForm(forms.Form):
    name = forms.CharField(label="Workspace name", max_length=30, required=True)
    password = forms.CharField(label="Workspace password", max_length=50, required=False, widget=PasswordInput)


