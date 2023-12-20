from django import forms
from shared_app.models import report

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ReportForm(forms.ModelForm):
    class Meta:
        model = report
        fields = ['text', 'image']