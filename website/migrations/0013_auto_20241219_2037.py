# Generated by Django 3.2.19 on 2024-12-19 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_lessonstats_bonus'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lessonstats',
            old_name='bonus',
            new_name='all_bonus',
        ),
        migrations.AddField(
            model_name='lessonstats',
            name='month_bonus',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
    ]
