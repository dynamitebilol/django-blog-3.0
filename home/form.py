from django import forms
from froala_editor.widgets import FroalaEditor
from .models import *


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ['content']



class NewCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['content']