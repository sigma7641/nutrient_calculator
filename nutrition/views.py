from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Nutrient
from .forms import NutrientForm, DateForm
import qrcode
from urllib.parse import urlparse, urlunparse, urlencode
from io import BytesIO
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.decorators import login_required
from user.models import Group
from django.contrib.auth.models import User
from django.contrib import messages
import logging
logger = logging.getLogger(__name__)
base_url = "http://192.168.1.2:8000"

@login_required
def index(request):
    nutrients = Nutrient.objects.filter(user=request.user)
    return render(request, 'nutrition/index.html', {'nutrients': nutrients})

@login_required
def create(request):
    group_members = get_members(request)
    if request.method == 'POST':
        form = NutrientForm(request.POST or None)
        if form.is_valid():
            ratio=form.cleaned_data['ratio']
            nutrient = Nutrient(
                name=form.cleaned_data['name'],
                calories=form.cleaned_data['calories']*ratio/100,
                protein=form.cleaned_data['protein']*ratio/100,
                fat=form.cleaned_data['fat']*ratio/100,
                carbohydrate=form.cleaned_data['carbohydrate']*ratio/100,
                price=form.cleaned_data['price']*ratio/100,
                user=form.cleaned_data['member'],
                )
            nutrient.save()
            messages.success(request, '保存しました。')
            return redirect(reverse('nutrition:index'))
        else:
            for field, error_messages in form.errors.items():
                for error_message in error_messages:
                    messages.error(request, f'{field}: {error_message}')
    elif  ("name" in request.GET) and ("calories" in request.GET) and ("protein" in request.GET) and ("fat" in request.GET) and ("carbohydrate" in request.GET) and ("price" in request.GET)  and ("ratio" in request.GET) :
        nutrient = Nutrient(
            name=request.GET.get('name'),
            calories=request.GET.get('calories'),
            protein=request.GET.get('protein'),
            fat=request.GET.get('fat'),
            carbohydrate=request.GET.get('carbohydrate'),
            price=request.GET.get('price'),
            ratio=request.GET.get('ratio'),
            )
        form = NutrientForm(instance=nutrient)
    else:
        form = NutrientForm()
    context = {
        'form': form,
        'members': group_members,
    }
    return render(request, 'nutrition/form.html', context)

@login_required
def detail(request, pk):
    nutrient = get_object_or_404(Nutrient, pk=pk)
    return render(request, 'nutrition/detail.html', {'nutrient': nutrient})

@login_required
def update(request, pk):
    group_members = get_members(request)
    nutrient = get_object_or_404(Nutrient, pk=pk)
    form = NutrientForm(request.POST or None, instance=nutrient)
    if form.is_valid():
        form.save()
        return redirect('nutrition:detail', pk=nutrient.pk)
    context = {
        'form': form,
        'members': group_members,
    }
    return render(request, 'nutrition/form.html', context)

@login_required
def delete(request, pk):
    nutrient = get_object_or_404(Nutrient, pk=pk)
    nutrient.delete()
    return redirect('nutrition:index')

@login_required
def create_qr(request):
    group_members = get_members(request)
    if request.method == 'POST':
        form = NutrientForm(request.POST or None)
        if form.is_valid():
            nutrient = Nutrient(
                name=form.cleaned_data['name'],
                calories=form.cleaned_data['calories'],
                protein=form.cleaned_data['protein'],
                fat=form.cleaned_data['fat'],
                carbohydrate=form.cleaned_data['carbohydrate'],
                price=form.cleaned_data['price'],
                ratio=form.cleaned_data['ratio'],
                )
            name=form.cleaned_data['name'],
            calories=form.cleaned_data['calories'],
            protein=form.cleaned_data['protein'],
            fat=form.cleaned_data['fat'],
            carbohydrate=form.cleaned_data['carbohydrate'],
            price=form.cleaned_data['price'],
            ratio=form.cleaned_data['ratio'],
        url = reverse('nutrition:create')
        params = {"name": name, "calories": calories, "protein": protein, "fat": fat, "carbohydrate": carbohydrate, "price": price, "ratio": ratio}
        # URLをパースして、クエリストリングを削除する
        parsed_url = urlparse(url)._replace(query=None)

        # 新しいクエリストリングを作成して、URLにくっつける
        url += "?"
        for key in params.keys():
            url += key + "=" + str(params.get(key)[0]) + "&"
        url = base_url + url[:-1]
        img = qrcode.make(url)

      # 画像を保存する
        buffer = BytesIO()
        img.save(buffer)
        buffer.seek(0)

        # レスポンスを返す
        return HttpResponse(buffer, content_type='image/png')
    else:
        form = NutrientForm()
    context = {
        'form': form,
        'members': group_members,
    }
    return render(request, 'nutrition/form_qr.html', context)

def aggregate_by_date(request):
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            nutrients = Nutrient.objects.filter(created_at__range=[start_date, end_date + timedelta(days=1)],user=request.user)
            total = Nutrient.objects.filter(created_at__range=[start_date, end_date + timedelta(days=1)],user=request.user).aggregate(
                calories=models.Sum('calories'),
                protein=models.Sum('protein'),
                fat=models.Sum('fat'),
                carbohydrate=models.Sum('carbohydrate'),
                price=models.Sum('price')
            )
            return render(request, 'aggregate_by_date_range.html', {'form': form, 'total': total, "nutrients": nutrients})
    else:
        form = DateForm(initial={
            'start_date': datetime.today() - timedelta(days=7),
            'end_date': datetime.today(),
        })
    return render(request, 'aggregate_by_date_range.html', {'form': form})

def get_members(request):
    groups = Group.objects.filter(members=request.user)
    group_members = []
    for group in groups:
        group_members += group.members.all()
    return group_members
