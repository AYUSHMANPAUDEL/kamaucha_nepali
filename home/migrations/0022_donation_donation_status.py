# Generated by Django 5.1.2 on 2024-10-20 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_donation_transcation_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='donation_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=20),
        ),
    ]