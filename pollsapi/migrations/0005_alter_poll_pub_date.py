# Generated by Django 3.2.7 on 2021-09-29 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pollsapi', '0004_alter_poll_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='pub_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
