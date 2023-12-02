# Generated by Django 4.2 on 2023-05-22 16:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docter', '0005_alter_doctorprofile_contact_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorprofile',
            name='consult_end',
            field=models.TimeField(default=datetime.time(22, 0)),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='consult_start',
            field=models.TimeField(default=datetime.time(14, 0)),
        ),
    ]
