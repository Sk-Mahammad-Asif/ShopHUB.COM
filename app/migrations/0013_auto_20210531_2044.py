# Generated by Django 3.1.6 on 2021-05-31 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20210531_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='rate',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]