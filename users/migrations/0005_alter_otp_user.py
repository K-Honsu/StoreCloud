# Generated by Django 4.2.2 on 2023-07-02 21:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_useraccount_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='otp', to=settings.AUTH_USER_MODEL),
        ),
    ]
