# Generated by Django 3.1.4 on 2020-12-04 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitutor', '0008_auto_20201204_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorie',
            name='date_insertion',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_insertion',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='date_insertion',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
