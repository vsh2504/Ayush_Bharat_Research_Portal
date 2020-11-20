from django import forms
from .models import Files

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ('file_title','description', 'document','project')