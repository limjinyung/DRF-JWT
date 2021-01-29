from django.urls import path, re_path
from .views import HelloView, create_task, task_list

urlpatterns = [
    path(r'hello/', HelloView.as_view(), name='hello'),
    # path(r'task_list/',view_tasks, name='view_tasks'),
    # re_path(r'create_task/<slug:name>/$', create_task, name='create_task'),
    path('task_list/', task_list),
    path('create_task/', create_task),
]
