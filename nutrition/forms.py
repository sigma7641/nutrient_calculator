from django import forms
from .models import Nutrient
from django.forms.widgets import DateInput
from django.contrib.auth.models import User
from user.models import Group
import logging
logger = logging.getLogger(__name__)

class NutrientForm(forms.ModelForm):
    name = forms.CharField(label='食品名', max_length=255, required=True)
    calories = forms.IntegerField(label='カロリー', widget=forms.HiddenInput, required=False)
    protein = forms.IntegerField(label='タンパク質', required=True)
    fat = forms.IntegerField(label='脂質', required=True)
    carbohydrate = forms.IntegerField(label='炭水化物', required=True)
    price = forms.IntegerField(label='値段', required=True)
    ratio = forms.IntegerField(label='比率(%)', required=True)
    member = forms.IntegerField(label='ユーザー', required=False)
    class Meta:
        model = Nutrient
        fields = ['name', 'calories', 'protein', 'fat', 'carbohydrate', 'price' , 'ratio', 'member']

    def clean(self):
        cleaned_data = super().clean()
        protein = cleaned_data.get('protein')
        fat = cleaned_data.get('fat')
        carbohydrate = cleaned_data.get('carbohydrate')
        price = cleaned_data.get('price')
        ratio = cleaned_data.get('ratio')
        member_id = cleaned_data.get('member')
        if protein is None or fat is None or carbohydrate is None or price is None or ratio is None:
            raise forms.ValidationError('タンパク質、脂質、炭水化物、値段、比率(%)は必須です。')
        else:
            calories = protein * 4 + fat * 9 + carbohydrate * 4
            cleaned_data['calories'] = calories
            cleaned_data['member'] = User.objects.get(id = member_id)
        return cleaned_data

class DateForm(forms.Form):
    #date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    start_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
