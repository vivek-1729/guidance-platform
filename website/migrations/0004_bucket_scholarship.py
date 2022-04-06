# Generated by Django 3.2.5 on 2022-01-06 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20210921_0728'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bucket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buckets', models.TextField(default="['general', 'english', 'engineering', 'business', 'governing', 'seen']")),
            ],
        ),
        migrations.CreateModel(
            name='Scholarship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('link', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=5000)),
            ],
        ),
    ]