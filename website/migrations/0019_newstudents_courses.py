# Generated by Django 3.2.19 on 2024-12-28 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0018_newstudents_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='newstudents',
            name='courses',
            field=models.ManyToManyField(blank=True, related_name='students_in_course', to='website.Course', verbose_name='Kursy'),
        ),
    ]
