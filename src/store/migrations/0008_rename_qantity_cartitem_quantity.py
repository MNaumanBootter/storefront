# Generated by Django 4.2.1 on 2023-05-23 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_cart_and_cartitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='qantity',
            new_name='quantity',
        ),
    ]
