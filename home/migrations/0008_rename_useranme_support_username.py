# Generated by Django 5.1.2 on 2024-10-17 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_support_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='support',
            old_name='useranme',
            new_name='username',
        ),
    ]