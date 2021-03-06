# Generated by Django 3.1.4 on 2021-01-08 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitutor', '0010_auto_20210101_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date_insertion',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='validation_status',
            field=models.BooleanField(default=False, verbose_name='commentaire(s) approuvé(s)'),
        ),
    ]
