# Generated by Django 5.1.6 on 2025-04-02 15:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Preferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genero', models.CharField(max_length=10)),
                ('objetivo', models.CharField(max_length=50)),
                ('edad', models.IntegerField()),
                ('peso', models.FloatField()),
                ('altura', models.FloatField()),
                ('nivel_actividad', models.CharField(max_length=20)),
                ('presupuesto', models.FloatField()),
                ('alergias', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account_preferences', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
