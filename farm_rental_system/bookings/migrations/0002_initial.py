# Generated by Django 5.1.1 on 2024-10-07 11:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bookings', '0001_initial'),
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='equipment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='equipment.equipment'),
        ),
    ]
