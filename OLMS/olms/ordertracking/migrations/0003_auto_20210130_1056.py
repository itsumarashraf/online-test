# Generated by Django 3.1.4 on 2021-01-30 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordertracking', '0002_auto_20210130_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackorder',
            name='ordertimestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
