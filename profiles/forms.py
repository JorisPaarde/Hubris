from django import forms

class player_select_form(forms.Form):
    selected = forms.CharField(widget=forms.HiddenInput)