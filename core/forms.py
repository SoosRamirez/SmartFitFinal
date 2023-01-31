from django import forms
from .models import BlogComment, PersonalInfo


class CommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = '__all__'


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = '__all__'
