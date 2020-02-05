# Generated by Django 2.2.9 on 2020-02-05 08:29

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_auto_20200130_0737'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'محصول', 'verbose_name_plural': 'محصولات'},
        ),
        migrations.AddField(
            model_name='productunit',
            name='variant',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]
