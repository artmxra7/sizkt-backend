# Generated by Django 3.0.7 on 2020-07-16 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mustahik', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mustahik',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mustahik',
            name='phone',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]