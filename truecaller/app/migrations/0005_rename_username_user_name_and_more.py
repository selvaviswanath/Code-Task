# Generated by Django 5.0.1 on 2024-01-13 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_globalcontact_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='username',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='globalcontact',
            name='contact_id',
        ),
    ]
