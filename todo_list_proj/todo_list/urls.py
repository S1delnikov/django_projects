"""Определяет схемы URL для todo_list"""

from django.urls import path
from . import views

app_name = 'todo_list'
urlpatterns = [
    # Домашняя страница
    path('', views.index, name='index'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/<int:task_id>/<int:subtask_id>/<str:status>/', views.savemark, name='savemark'),
    path('tasks/update_task/<int:task_id>/<int:subtask_id>/<str:text>/', views.update_task, name='update_task'),
    # path('tasks/new_subtask/<int:task_id>/<str:text>/', views.new_subtask, name='new_subtask'),
    path('tasks/new_subtask/', views.new_subtask, name='new_subtask'),
    path('tasks/delete_subtask/', views.delete_subtask, name='delete_subtask'),
    path('tasks/get_csrftoken/', views.get_csrftoken, name='get_csrftoken'),
    path('tasks/new_task/', views.new_task, name='new_task'),
    path('tasks/delete_task/', views.delete_task, name='delete_task'),
    path('tasks/update_task_data/', views.update_task_data, name='update_task_data/'),
]