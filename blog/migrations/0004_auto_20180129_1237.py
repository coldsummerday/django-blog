# Generated by Django 2.0 on 2018-01-29 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180125_0934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='url',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
    ]