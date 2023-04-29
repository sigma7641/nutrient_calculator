from django.urls import path
from .views import create_group, register, group_list, delete_group

app_name = 'user'

urlpatterns = [
    path('', create_group, name='group_list'),
    path('create_group/', create_group, name='create_group'),
    path('register/', register, name='register'),
    path('group_list/', group_list, name='group_list'),
    path('groups/<int:group_id>/delete/', delete_group, name='delete_group'),
]

