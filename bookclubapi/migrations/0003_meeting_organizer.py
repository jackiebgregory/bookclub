# Generated by Django 4.0.3 on 2022-03-15 01:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookclubapi', '0002_remove_meeting_reader_meeting_readers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='organizer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='hosting', to='bookclubapi.reader'),
        ),
    ]
