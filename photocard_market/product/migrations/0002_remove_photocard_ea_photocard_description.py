# Generated by Django 4.0 on 2024-07-18 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="photocard",
            name="ea",
        ),
        migrations.AddField(
            model_name="photocard",
            name="description",
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
