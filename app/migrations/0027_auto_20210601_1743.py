# Generated by Django 3.1.6 on 2021-06-01 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20210601_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='rate',
            field=models.IntegerField(default=4),
        ),
    ]
