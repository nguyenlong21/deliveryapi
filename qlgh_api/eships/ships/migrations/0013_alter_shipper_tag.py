# Generated by Django 4.0.4 on 2022-05-10 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ships', '0012_alter_action_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipper',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='shippers', to='ships.tag'),
        ),
    ]