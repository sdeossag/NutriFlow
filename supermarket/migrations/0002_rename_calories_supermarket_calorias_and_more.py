# Generated by Django 5.1.6 on 2025-04-23 03:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supermarket', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supermarket',
            old_name='calories',
            new_name='calorias',
        ),
        migrations.RenameField(
            model_name='supermarket',
            old_name='carbs',
            new_name='carbohidratos',
        ),
        migrations.RenameField(
            model_name='supermarket',
            old_name='fat',
            new_name='grasas',
        ),
        migrations.RenameField(
            model_name='supermarket',
            old_name='image',
            new_name='imagen',
        ),
        migrations.RenameField(
            model_name='supermarket',
            old_name='name_supermarket',
            new_name='marca_producto',
        ),
        migrations.RenameField(
            model_name='supermarket',
            old_name='product_brand',
            new_name='nombre_producto',
        ),
        migrations.RenameField(
            model_name='supermarket',
            old_name='product_name',
            new_name='nombre_supermercado',
        ),
        migrations.RenameField(
            model_name='supermarket',
            old_name='product_price',
            new_name='precio_producto',
        ),
        migrations.RenameField(
            model_name='supermarket',
            old_name='protein',
            new_name='proteinas',
        ),
    ]
