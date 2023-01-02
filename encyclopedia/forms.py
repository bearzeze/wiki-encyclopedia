from django import forms

class CreateNewEntryForm(forms.Form):
    title = forms.CharField(label="Type Title of New Entry", max_length=100, required=True, widget=forms.TextInput(attrs={"class":"title-new"}))
    content = forms.CharField(label="Content:",  required=True,  widget=forms.Textarea)
    

class EditEntryForm(forms.Form):
    title = forms.CharField(label="Edit Title of Entry", max_length=100, required=True, widget=forms.TextInput(attrs={"class":"title-new"}))
    content = forms.CharField(label="Content:", required=True, widget=forms.Textarea)
    