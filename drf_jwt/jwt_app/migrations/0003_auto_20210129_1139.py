# Generated by Django 3.1.5 on 2021-01-29 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_app', '0002_remove_developer_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='name',
            new_name='todo',
        ),
    ]
