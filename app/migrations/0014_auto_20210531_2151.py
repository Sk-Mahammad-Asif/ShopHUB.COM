# Generated by Django 3.1.6 on 2021-05-31 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20210531_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='app.product'),
        ),
    ]