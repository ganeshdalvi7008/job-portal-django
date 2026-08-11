from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    resume = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write a brief cover letter describing your fit for this role...'}),
        }
