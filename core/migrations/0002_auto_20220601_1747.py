# Generated by Django 3.2.13 on 2022-06-01 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='unit',
            old_name='_type',
            new_name='type',
        ),
        migrations.AlterField(
            model_name='field',
            name='abr',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
