# Generated by Django 4.2.1 on 2023-05-29 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('week9_app', '0004_remove_user_db_pass2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_db',
            name='pass1',
            field=models.CharField(max_length=128),
        ),
    ]
