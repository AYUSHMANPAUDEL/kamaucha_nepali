# Generated by Django 5.1.2 on 2024-10-19 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_alter_alert_alert_sound'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='donation_message',
            field=models.TextField(default=''),
        ),
    ]
