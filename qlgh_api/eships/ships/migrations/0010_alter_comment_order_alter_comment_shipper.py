# Generated by Django 4.0.4 on 2022-05-10 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ships', '0009_alter_comment_shipper_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ships.order'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='shipper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ships.shipper'),
        ),
    ]
