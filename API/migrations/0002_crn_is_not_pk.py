# Generated by Django 2.1.4 on 2018-12-19 12:26

from django.db import migrations, models
from time import time

class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knowngrade',
            name='course_key',
            field=models.CharField(max_length=7),
        ),
        migrations.AddField(
            model_name='knowngrade',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
