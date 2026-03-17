from django import forms
from .models import Rack, Shelf


class RackForm(forms.ModelForm):
    class Meta:
        model = Rack
        fields = ['name', 'category', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g. A, B, C',
                'style': 'text-transform: uppercase;'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Lipsticks, Foundations'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional description...'
            }),
        }


class ShelfForm(forms.ModelForm):
    class Meta:
        model = Shelf
        fields = ['rack', 'code', 'description']
        widgets = {
            'rack': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'code': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g. A1, A2',
                'style': 'text-transform: uppercase;'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional description...'
            }),
        }


class BulkShelfForm(forms.Form):
    rack = forms.ModelChoiceField(
        queryset=Rack.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
    )
    count = forms.IntegerField(
        min_value=1, max_value=20,
        initial=4,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
        label='Number of shelves to create'
    )
