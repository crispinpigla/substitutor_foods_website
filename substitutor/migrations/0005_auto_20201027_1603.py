# Generated by Django 3.1.2 on 2020-10-27 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("substitutor", "0004_auto_20201021_0237")]

    operations = [
        migrations.RemoveField(model_name="favorite", name="recherche"),
        migrations.AddField(
            model_name="favorite",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product",
                to="substitutor.product",
            ),
        ),
        migrations.AlterField(
            model_name="categorie", name="name", field=models.CharField(max_length=255)
        ),
        migrations.AlterField(
            model_name="favorite",
            name="substitut",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="substitut",
                to="substitutor.product",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="categorie",
            field=models.ManyToManyField(
                blank=True, related_name="product", to="substitutor.Categorie"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="store",
            field=models.ManyToManyField(
                blank=True, related_name="product", to="substitutor.Store"
            ),
        ),
        migrations.AlterField(
            model_name="store", name="name", field=models.CharField(max_length=255)
        ),
    ]
