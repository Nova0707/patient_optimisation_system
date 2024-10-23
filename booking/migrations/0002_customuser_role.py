# Generated by Django 3.2.12 on 2024-10-21 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Doctor', 'Doctor'), ('Receptionist', 'Receptionist')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]
