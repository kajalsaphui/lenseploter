# Generated by Django 3.0 on 2021-06-24 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210624_0207'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='user_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
