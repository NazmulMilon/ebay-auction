# Generated by Django 3.2.8 on 2021-12-29 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='hashed_id',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
