# Generated by Django 3.2.5 on 2021-07-12 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210712_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='biography',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
