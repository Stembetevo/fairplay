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
                    'placeholder' : 'rating from 50-100',
                    'min': '50',
                    'max': '100'
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

    