from django import forms
from .models import Product
from racks.models import Rack, Shelf


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'rack', 'shelf', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g. Lipstick Ruby',
                'autofocus': True,
            }),
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Lakme, Maybelline',
            }),
            'rack': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_rack',
            }),
            'shelf': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_shelf',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional notes...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rack'].empty_label = '— Select Rack —'
        self.fields['shelf'].empty_label = '— Select Shelf —'
        self.fields['rack'].required = False
        self.fields['shelf'].required = False
        # Filter shelves based on selected rack
        rack_id = None
        if self.instance.pk and self.instance.rack:
            rack_id = self.instance.rack.pk
        elif self.data.get('rack'):
            rack_id = self.data.get('rack')
        if rack_id:
            self.fields['shelf'].queryset = Shelf.objects.filter(rack_id=rack_id)
        else:
            self.fields['shelf'].queryset = Shelf.objects.none()


class MoveProductForm(forms.Form):
    new_rack = forms.ModelChoiceField(
        queryset=Rack.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select form-select-lg', 'id': 'id_new_rack'}),
        label='New Rack',
    )
    new_shelf = forms.ModelChoiceField(
        queryset=Shelf.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select form-select-lg', 'id': 'id_new_shelf'}),
        label='New Shelf',
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
        rack_id = kwargs.pop('rack_id', None)
        super().__init__(*args, **kwargs)
        if rack_id:
            self.fields['new_shelf'].queryset = Shelf.objects.filter(rack_id=rack_id)
        self.fields['new_rack'].empty_label = '— Select Rack —'
        self.fields['new_shelf'].empty_label = '— Select Shelf —'


class QuickQuantityForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'min': '0'}),
    )
