# Generated by Django 3.2.9 on 2021-11-04 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0019_auto_20211104_1959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='family',
        ),
        migrations.AddField(
            model_name='party',
            name='category',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]