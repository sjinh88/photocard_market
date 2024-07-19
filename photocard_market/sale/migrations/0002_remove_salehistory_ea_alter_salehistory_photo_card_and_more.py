# Generated by Django 4.0 on 2024-07-18 17:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0002_remove_photocard_ea_photocard_description"),
        ("sale", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="salehistory",
            name="ea",
        ),
        migrations.AlterField(
            model_name="salehistory",
            name="photo_card",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="photocard",
                to="product.photocard",
            ),
        ),
        migrations.AlterField(
            model_name="salehistory",
            name="price",
            field=models.PositiveIntegerField(help_text="1개당 가격"),
        ),
        migrations.AlterField(
            model_name="salehistory",
            name="state",
            field=models.CharField(
                choices=[("E", "판매완료"), ("B", "판매중")], default="B", max_length=1
            ),
        ),
    ]