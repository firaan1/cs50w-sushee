# Generated by Django 2.0.3 on 2018-09-01 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0029_userinput'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinput',
            name='review',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
