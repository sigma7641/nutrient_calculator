from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Nutrient
from .forms import NutrientForm


def index(request):
    nutrients = Nutrient.objects.all()
    return render(request, 'nutrition/index.html', {'nutrients': nutrients})

def create(request):
    if request.method == 'POST':
        form = NutrientForm(request.POST or None)
        if form.is_valid():
            nutrient = Nutrient(
                name=form.cleaned_data['name'],
                calories=form.cleaned_data['calories'],
                protein=form.cleaned_data['protein'],
                fat=form.cleaned_data['fat'],
                carbohydrate=form.cleaned_data['carbohydrate'],
            )
            nutrient.save()
            return redirect(reverse('nutrition:index'))
    else:
        form = NutrientForm()

    context = {
        'form': form
    }
    return render(request, 'nutrition/form.html', {'form': form})

def detail(request, pk):
    nutrient = get_object_or_404(Nutrient, pk=pk)
    return render(request, 'nutrition/detail.html', {'nutrient': nutrient})

def update(request, pk):
    nutrient = get_object_or_404(Nutrient, pk=pk)
    form = NutrientForm(request.POST or None, instance=nutrient)
    if form.is_valid():
        form.save()
        return redirect('nutrition:detail', pk=nutrient.pk)
    return render(request, 'nutrition/form.html', {'form': form})

def delete(request, pk):
    nutrient = get_object_or_404(Nutrient, pk=pk)
    nutrient.delete()
    return redirect('nutrition:index')
