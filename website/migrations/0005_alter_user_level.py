# Generated by Django 3.2.19 on 2024-12-15 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_user_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='level',
            field=models.CharField(blank=True, choices=[('Podstawa', 'Podstawa'), ('Rozszerzenie', 'Rozszerzenie')], max_length=50, verbose_name='Poziom'),
        ),
    ]
