# Generated by Django 3.2.5 on 2022-01-06 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_bucket_scholarship'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='name',
            field=models.CharField(max_length=1001),
        ),
    ]
