# Generated by Django 3.2.8 on 2021-12-29 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='hashed_id',
            field=models.CharField(blank=True, db_index=True, max_length=16, null=True),
        ),
    ]
