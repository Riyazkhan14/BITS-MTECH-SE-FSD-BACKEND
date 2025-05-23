# Generated by Django 5.1.7 on 2025-04-28 14:35

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('class_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(blank=True, max_length=1000)),
                ('name', models.CharField(blank=True, max_length=1200)),
                ('is_delete', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('Class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='class_app.classes')),
            ],
        ),
    ]
