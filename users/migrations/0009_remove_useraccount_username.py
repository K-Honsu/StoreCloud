# Generated by Django 4.2.2 on 2023-07-06 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_useraccount_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccount',
            name='username',
        ),
    ]
