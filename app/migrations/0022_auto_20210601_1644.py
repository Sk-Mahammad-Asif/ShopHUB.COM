# Generated by Django 3.1.6 on 2021-06-01 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20210601_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='rate',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
