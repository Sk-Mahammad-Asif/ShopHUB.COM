# Generated by Django 3.1.6 on 2021-05-25 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20210525_1127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_image_child1_min',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_image_child2_min',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_image_child3_min',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_image_min',
        ),
    ]
