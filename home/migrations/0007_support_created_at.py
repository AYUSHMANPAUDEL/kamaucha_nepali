# Generated by Django 5.1.2 on 2024-10-17 05:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_support_ticket_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='support',
            name='created_at',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
