
from django import forms
from .models import Note


class CreateNoteForm(forms.Form):
    title = forms.CharField(required=False)
    content = forms.CharField(widget=forms.Textarea, required=False)
    class Meta():
        model = Note
        fields = ['title', 'content']

    