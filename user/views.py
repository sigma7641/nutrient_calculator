from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import GroupForm
from .models import Group
import logging
logger = logging.getLogger(__name__)

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.user, request.POST)
        if form.is_valid():
            logger.critical('form is valid')
            group = form.save(commit=False)
            group.owner = request.user
            logger.critical('{request.user}form is valid')
            group.save()
            group.members.add(request.user)
            messages.success(request, f'グループ {group.name}が作成されました！')
            #return render(request, 'group_list.html')
            return redirect(reverse('user:group_list'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field} {error}")
            return render(request, 'create_group.html', {'form': form})
    else:
        form = GroupForm(request.user)
    return render(request, 'create_group.html', {'form': form})

@login_required
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        group_id = request.POST.get('group_id')
        user = User.objects.get(username=username)
        group = Group.objects.get(id=group_id)
        group.members.add(user)
        #form.save_m2m()
        messages.success(request, f'{username} さんを {group.name} グループに登録しました')
        return redirect(reverse('user:group_list'))
    groups = Group.objects.filter(members=request.user)
    return render(request, 'register.html', {'groups': groups})

@login_required
def group_list(request):
    user = request.user
    groups = Group.objects.filter(members=request.user)
    return render(request, 'group_list.html', {'groups': groups})

@login_required
def delete_group(request, group_id):
    group = Group.objects.get(id=group_id)
    group.delete()
    return redirect(reverse('user:group_list'))
