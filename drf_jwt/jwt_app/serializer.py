from rest_framework import serializers
from .models import Task

class TaskSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('todo', 'description')