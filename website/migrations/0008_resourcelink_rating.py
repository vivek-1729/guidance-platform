# Generated by Django 3.2.5 on 2022-02-13 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_scholarship'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourcelink',
            name='rating',
            field=models.TextField(null=True),
        ),
    ]
