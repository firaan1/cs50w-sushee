# Generated by Django 2.0.3 on 2018-09-01 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0032_auto_20180901_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinput',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='input_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
