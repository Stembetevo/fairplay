from django import forms
from .models import Player, Team
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PlayerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Search for Username...',
            'autocomplete':'on'
        }),
        help_text='Enter the username of a registered player'
    )
    position_override = forms.ChoiceField(
        choices=Player.Position.choices,
        required=False,
        widget = forms.Select(attrs={
            'class':'form-control'
        }),
    )
    rating = forms.IntegerField(
        initial=70,
        min_value=50,
        max_value=100,
        widget = forms.NumberInput(attrs={
            'class':'form-control',
            'placeholder':'50-100',
            'min':'50',
            'max':'100'
        })
    )
    

class TeamForm(forms.Form):
    number_of_teams = forms.IntegerField(
        min_value=2,
        max_value=10,
        label = 'No of Teams',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter number of Teams (2-10)'
        })
    )

    def __init__(self, *args, **kwargs):
        num_of_teams = kwargs.pop('num_of_teams', 2)
        super().__init__(*args, **kwargs)

        for i in range(1, num_of_teams+1):
            self.fields[f"team_{i}_name"] = forms.CharField(
                max_length=100,
                label=f'Team {i} Name',
                widget=forms.TextInput(attrs={
                    'class':'form-control',
                    'placeholder':f'Enter name of Team {i} '
                })
            )

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address',
        }),
        help_text='Required. Enter a valid email address.'
    )
    preferred_position = forms.ChoiceField(
        choices=Player.Position.choices,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        help_text='Select your preferred playing position'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'preferred_position']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password',
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user.profile.preferred_position = self.cleaned_data['preferred_position']
            user.profile.save()
        return user

    