# Generated by Django 5.0.6 on 2024-05-17 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='chart/'),
        ),
    ]
