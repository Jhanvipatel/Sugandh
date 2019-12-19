from django import forms

class sizeform(forms.Form):
    size = forms.CharField(max_length=10, initial='avil page')

