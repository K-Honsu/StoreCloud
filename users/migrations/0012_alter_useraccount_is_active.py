# Generated by Django 4.2.2 on 2023-07-06 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_useraccount_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
