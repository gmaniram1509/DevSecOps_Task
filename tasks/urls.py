from django.urls import path
from . import views

urlpatterns = [
    # Task URLs
    path('', views.task_list, name='task_list'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/create/', views.task_create, name='task_create'),
    path('task/<int:pk>/update/', views.task_update, name='task_update'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
    
    # Time Entry URLs
    path('task/<int:task_pk>/time-entry/create/', views.time_entry_create, name='time_entry_create'),
    path('time-entry/<int:pk>/update/', views.time_entry_update, name='time_entry_update'),
    path('time-entry/<int:pk>/delete/', views.time_entry_delete, name='time_entry_delete'),
]

