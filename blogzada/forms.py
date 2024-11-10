from django import forms
from django.contrib.auth.models import User  # Certifique-se de usar apenas o User do Django
from .models import Post  # Use apenas Post do seu próprio app

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        return cleaned_data

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
        
        labels = {
            'title': 'Title',
            'content': 'Content',
        }
        
