# Generated by Django 5.0.1 on 2024-01-13 12:55

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_user_alter_contact_is_spam_alter_contact_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalcontact',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]