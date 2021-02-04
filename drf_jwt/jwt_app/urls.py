from django.urls import path, re_path
from .views import create_task, get_task, task_list, update_task, delete_task
from .views import get_developer, developer_list, create_developer, update_developer, delete_developer
from .views import image_upload, document_upload

urlpatterns = [
    # path(r'hello/', HelloView.as_view(), name='hello'),
    path('task_list/', task_list),
    path('get_task/', get_task),
    path('create_task/', create_task),
    path('update_task/<int:task_id>', update_task),
    path('delete_task/<int:task_id>', delete_task),
    path('developer_list/', developer_list),
    path('get_developer/', get_developer),
    path('create_developer/', create_developer),
    path('update_developer/<int:developer_id>', update_developer),
    path('delete_developer/<int:developer_id>', delete_developer),
    re_path('image_upload/', image_upload),
    re_path('document_upload/', document_upload),
]
