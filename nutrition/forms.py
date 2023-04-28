from django import forms
from .models import Nutrient

class NutrientForm(forms.ModelForm):
    name = forms.CharField(label='食品名', max_length=255, required=True)
    calories = forms.IntegerField(label='カロリー', widget=forms.HiddenInput, required=False)
    protein = forms.IntegerField(label='タンパク質', required=True)
    fat = forms.IntegerField(label='脂質', required=True)
    carbohydrate = forms.IntegerField(label='炭水化物', required=True)

    class Meta:
        model = Nutrient
        fields = ['name', 'calories', 'protein', 'fat', 'carbohydrate']

    def clean(self):
        cleaned_data = super().clean()
        protein = cleaned_data.get('protein')
        fat = cleaned_data.get('fat')
        carbohydrate = cleaned_data.get('carbohydrate')
        if protein is None or fat is None or carbohydrate is None:
            raise forms.ValidationError('タンパク質、脂質、炭水化物は必須です。')
        else:
            calories = protein * 4 + fat * 9 + carbohydrate * 4
            cleaned_data['calories'] = calories
        return cleaned_data
