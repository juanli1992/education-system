# Generated by Django 2.2 on 2019-04-08 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0013_auto_20190408_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lib',
            name='DateTime',
            field=models.DateTimeField(),
        ),
    ]