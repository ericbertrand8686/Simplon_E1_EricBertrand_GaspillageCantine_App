# Generated by Django 4.2.1 on 2023-06-01 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cantinedata', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fréquentation',
            name='annee',
        ),
    ]
