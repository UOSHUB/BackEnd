# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name="KnownGrade",
            fields=[
                ("course_key", models.CharField(max_length=7, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                ("sid", models.CharField(max_length=9, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name="knowngrade",
            name="student",
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, to="Requests.Student"),
        ),
    ]
