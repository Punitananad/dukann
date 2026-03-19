from django import forms
from .models import Product
from racks.models import Wall, Rack


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'subcategory', 'tags', 'search_keywords', 'wall', 'rack', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g. Lipstick Ruby',
                'autofocus': True,
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Makeup, Skincare, Hair',
            }),
            'subcategory': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Lip Liner, BB Cream, Anti-Aging',
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. matte, waterproof, spf',
            }),
            'search_keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. face wash cleanser oily skin',
            }),
            'wall': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_wall',
            }),
            'rack': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_rack',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional notes...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['wall'].empty_label = '— Select Wall —'
        self.fields['rack'].empty_label = '— Select Rack —'
        self.fields['wall'].required = False
        self.fields['rack'].required = False
        wall_id = None
        if self.instance.pk and self.instance.wall:
            wall_id = self.instance.wall.pk
        elif self.data.get('wall'):
            wall_id = self.data.get('wall')
        if wall_id:
            self.fields['rack'].queryset = Rack.objects.filter(wall_id=wall_id)
        else:
            self.fields['rack'].queryset = Rack.objects.none()


class MoveProductForm(forms.Form):
    new_wall = forms.ModelChoiceField(
        queryset=Wall.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select form-select-lg', 'id': 'id_new_wall'}),
        label='New Wall',
    )
    new_rack = forms.ModelChoiceField(
        queryset=Rack.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select form-select-lg', 'id': 'id_new_rack'}),
        label='New Rack',
        required=False,
    )
    notes = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Reason for moving (optional)...',
        }),
    )

    def __init__(self, *args, **kwargs):
        wall_id = kwargs.pop('wall_id', None)
        super().__init__(*args, **kwargs)
        if wall_id:
            self.fields['new_rack'].queryset = Rack.objects.filter(wall_id=wall_id)
        self.fields['new_wall'].empty_label = '— Select Wall —'
        self.fields['new_rack'].empty_label = '— Select Rack —'


class QuickQuantityForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'min': '0'}),
    )
