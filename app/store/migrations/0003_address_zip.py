# Generated by Django 4.1.7 on 2023-03-29 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_price_product_unit_price_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='zip',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]