from django import forms
from .models import Wall, Rack


class WallForm(forms.ModelForm):
    class Meta:
        model = Wall
        fields = ['name', 'category', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g. A, B, C or North, South',
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

    def clean_name(self):
        return self.cleaned_data['name'].upper()


class WallWithRacksForm(WallForm):
    rack_count = forms.IntegerField(
        min_value=0, max_value=50,
        initial=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'min': '0', 'max': '50',
            'id': 'id_rack_count'
        }),
        label='Number of racks to create (0 = add manually later)',
        help_text='Leave 0 to add racks manually after creating the wall'
    )

    class Meta:
        model = Wall
        fields = ['name', 'category', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g. A, B, C or North, South',
                'style': 'text-transform: uppercase;'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Lipsticks, Foundations'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Optional description...'
            }),
        }


class RackForm(forms.ModelForm):
    class Meta:
        model = Rack
        fields = ['wall', 'code', 'description']
        widgets = {
            'wall': forms.Select(attrs={'class': 'form-select form-select-lg'}),
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

    def clean_code(self):
        return self.cleaned_data['code'].upper()


class BulkRackForm(forms.Form):
    wall = forms.ModelChoiceField(
        queryset=Wall.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
    )
    count = forms.IntegerField(
        min_value=1, max_value=50,
        initial=4,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
        label='Number of racks to create'
    )
