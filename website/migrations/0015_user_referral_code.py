# Generated by Django 3.2.19 on 2024-12-19 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_auto_20241219_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='referral_code',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
