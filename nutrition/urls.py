from django.contrib import admin
from django.urls import path
from nutrition import views

app_name = 'nutrition'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('aggregate/', views.aggregate_by_date, name='aggregate'),
    path('qrcreate/', views.create_qr, name='qrcreate'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
]

