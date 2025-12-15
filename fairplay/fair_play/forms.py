from django import forms
from .models import Player, Team

class PlayerCreationForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'position', 'rating']
        widgets = {
            'name' : forms.TextInput(
                attrs={
                'class':'form-control',
                'placeholder': 'Enter Player name'
            }),
            'rating' : forms.NumberInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' : 'rating from 1-5',
                    'min': '1',
                    'max': '5'
                }
            ),
            'position': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

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
    