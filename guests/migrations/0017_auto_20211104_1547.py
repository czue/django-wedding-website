# Generated by Django 3.2.9 on 2021-11-04 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0016_party_rehearsal_dinner'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='side',
            field=models.CharField(choices=[('kim', 'Kim'), ('jake', 'Jake')], default='', max_length=10),
        ),
        migrations.AddField(
            model_name='party',
            name='side',
            field=models.CharField(choices=[('kim', 'Kim'), ('jake', 'Jake')], default='', max_length=10),
        ),
    ]