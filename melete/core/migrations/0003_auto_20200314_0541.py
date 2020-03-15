# Generated by Django 2.2.11 on 2020-03-14 05:41

from django.db import migrations, models
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200313_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credentials',
            name='password',
            field=encrypted_model_fields.fields.EncryptedCharField(db_column='password'),
        ),
        migrations.AlterField(
            model_name='credentials',
            name='username',
            field=models.CharField(db_column='username', max_length=255),
        ),
    ]
