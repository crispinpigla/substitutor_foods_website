# Generated by Django 3.1.2 on 2020-10-21 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("substitutor", "0002_product_url_image")]

    operations = [
        migrations.RenameField(
            model_name="product", old_name="magasin", new_name="store"
        ),
        migrations.AddField(
            model_name="product", name="code", field=models.IntegerField(null=True)
        ),
    ]