# Generated by Django 3.1.4 on 2021-02-01 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_app', '0003_auto_20210129_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer',
            name='name',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AlterField(
            model_name='task',
            name='todo',
            field=models.CharField(default=None, max_length=20),
        ),
    ]