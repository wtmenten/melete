# Generated by Django 2.2.11 on 2020-03-13 02:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='threadseries',
            name='date_processed',
        ),
        migrations.AddField(
            model_name='thread',
            name='date',
            field=models.DateTimeField(db_column='date', default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
