# Generated by Django 3.0 on 2019-12-15 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeclock', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useractivity',
            options={'verbose_name': 'User Activity', 'verbose_name_plural': 'User Actitvities'},
        ),
    ]