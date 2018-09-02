# Generated by Django 2.0.3 on 2018-09-02 17:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shopping', '0036_remove_userinput_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinput',
            name='dresstype',
            field=models.CharField(default='daree', max_length=25),
        ),
        migrations.AlterUniqueTogether(
            name='userinput',
            unique_together={('user', 'dresstype', 'dresspk')},
        ),
    ]