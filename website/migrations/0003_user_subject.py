# Generated by Django 3.2.19 on 2024-12-14 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20241214_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.topic'),
        ),
    ]
