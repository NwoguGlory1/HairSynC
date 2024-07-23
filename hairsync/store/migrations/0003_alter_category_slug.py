# Generated by Django 5.1.dev20240319090312 on 2024-03-20 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_category_slug_alter_product_price_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(
                default="default-category-slug",
                editable=False,
                max_length=255,
                unique=True,
            ),
        ),
    ]
