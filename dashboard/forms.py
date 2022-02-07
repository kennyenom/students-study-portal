from dataclasses import fields
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','message']
        help_texts={
            'title':None,
            'message':None
        }


class CreateHomeWork(forms.ModelForm):
    class Meta:
        model = Homework
        fields =['subject','title','desc','due','is_finished']
        widgets = {
          'desc': forms.Textarea(attrs={'rows':4, 'cols':5}),
        }

class YoutubeForm(forms.Form):
    text = forms.CharField(label='search anything here')

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title']
        

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
        help_texts ={
            'username':None,
            'password1':None,
            'password2':None,
        }
    
    def __init__(self,*args,**kwargs):
        super(RegisterForm,self).__init__(*args,**kwargs)
        for fieldname in ['username','password1','password2']:
            self.fields[fieldname].help_text = None
