from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Task(models.Model):
    todo = models.CharField(max_length=20, default=None)
    description = models.CharField(max_length=50)

    def __str__(self):
        return '%s %s' % (self.todo, self.description)


class Developer(models.Model):
    POSITIONS = (
        ('PM', 'Project Manager'),
        ('QA', 'Quality Assurance'),
        ('SD', 'Software Developer'),
    )
    name = models.CharField(max_length=20, default=None)
    email = models.CharField(max_length=30, null=True)
    task = models.ManyToManyField('Task', null=True)
    position = models.CharField(max_length=20, choices=POSITIONS, null=True, default=POSITIONS[2][0])

    def __str__(self):
        return '%s %s %s' % (self.name, self.task, self.position)
