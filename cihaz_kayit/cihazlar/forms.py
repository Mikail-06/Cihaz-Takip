from django import forms
from .models import Cihaz

class CihazForm(forms.ModelForm):
    class Meta:
        model = Cihaz
        fields = [
            'marka',
            'model',
            'destek_durumu',
            'aciklama',
            'musteri',
            'test_durumu',
            'platform',
            'note',
            'supported_features',
            'model_note',
        ]
        widgets = {
            'aciklama': forms.TextInput(attrs={'placeholder': ''}),
            'musteri': forms.TextInput(attrs={'placeholder': ''}),
            'test_durumu': forms.TextInput(attrs={'placeholder': ''}),
            'platform': forms.TextInput(attrs={'placeholder': ''}),
            'note': forms.Textarea(attrs={'placeholder': ''}),
            'supported_features': forms.Textarea(attrs={'placeholder': ''}),
            'model_note': forms.Textarea(attrs={'placeholder': ''}),
        }

class UploadFileForm(forms.Form):
    file = forms.FileField(label='CSV veya Excel Dosyası Seç')
