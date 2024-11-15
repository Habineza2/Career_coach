from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = [
            'name',
            'email',
            'password',
            'career_goal',
            'skills',
            'experience_level',
            'industry_preference',
            'profile_picture'
        ]




# forms.py

from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary', 'is_active']
