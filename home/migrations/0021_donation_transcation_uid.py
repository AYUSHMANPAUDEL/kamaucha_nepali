# Generated by Django 5.1.2 on 2024-10-20 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_alter_donation_page_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='transcation_uid',
            field=models.TextField(default=''),
        ),
    ]
