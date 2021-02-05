from django.contrib import admin
from django.contrib.sessions.models import Session
from jwt_app.models import Task, Developer

# Register your models here.
admin.site.register([Task, Developer, Session])