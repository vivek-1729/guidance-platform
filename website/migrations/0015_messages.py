# Generated by Django 3.2.5 on 2022-02-23 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_remove_student_badges'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('time', models.TimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('receiver_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='website.student')),
                ('sender_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='website.student')),
            ],
            options={
                'ordering': ('timestamp',),
            },
        ),
    ]
