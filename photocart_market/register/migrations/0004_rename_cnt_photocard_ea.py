# Generated by Django 4.0 on 2024-07-16 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_delete_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photocard',
            old_name='cnt',
            new_name='ea',
        ),
    ]
