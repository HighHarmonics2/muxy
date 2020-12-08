# Generated by Django 3.1.4 on 2020-12-08 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_delete_streamingservice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='participants',
        ),
        migrations.RemoveField(
            model_name='stream',
            name='participant',
        ),
        migrations.AddField(
            model_name='stream',
            name='publisher_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='stream',
            name='publisher_name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.DeleteModel(
            name='Participant',
        ),
    ]