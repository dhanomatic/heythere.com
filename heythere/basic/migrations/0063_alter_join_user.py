# Generated by Django 4.0.5 on 2022-07-19 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0062_join'),
    ]

    operations = [
        migrations.AlterField(
            model_name='join',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.userregister'),
        ),
    ]