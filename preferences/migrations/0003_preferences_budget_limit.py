# Generated by Django 5.1.5 on 2025-03-14 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preferences', '0002_alter_preferences_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='preferences',
            name='budget_limit',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
