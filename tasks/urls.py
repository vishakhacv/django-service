from django.urls import path
from . import views

urlpatterns = [
    path('check-overdue/', views.check_overdue, name='check-overdue'),
    path('tasks/<int:task_id>/close/', views.close_overdue_task, name='close-overdue-task'),
    path('overdue-tasks/', views.list_overdue_tasks, name='list-overdue-tasks'),
]
