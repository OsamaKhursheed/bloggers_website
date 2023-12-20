from django import forms
from .models import blog_maker
from shared_app.models import Blog
class RegistrationForm(forms.ModelForm):
    class Meta:
        model = blog_maker
        fields = ['first_name', 'last_name', 'father_name', 'profile_image', 'email', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'image']

class BlogUpdateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'image']