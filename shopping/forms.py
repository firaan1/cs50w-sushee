from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document', )

class DocumentForm2(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
    )
