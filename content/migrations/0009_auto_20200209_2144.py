# Generated by Django 2.2.9 on 2020-02-09 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_auto_20200209_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]