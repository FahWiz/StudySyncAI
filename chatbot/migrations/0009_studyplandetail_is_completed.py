# Generated by Django 5.1.6 on 2025-03-18 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0008_studyplan_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='studyplandetail',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
