# Generated by Django 3.1.4 on 2021-01-01 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('substitutor', '0009_auto_20201204_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_favorite', to='substitutor.product'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu_text', models.TextField()),
                ('validation_status', models.BooleanField(default=False, verbose_name='demande traitée ?')),
                ('commentator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentator', to='substitutor.account')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='substitutor.product')),
            ],
        ),
    ]
