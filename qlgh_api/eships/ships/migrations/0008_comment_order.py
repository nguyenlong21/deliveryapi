# Generated by Django 4.0.4 on 2022-05-09 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ships', '0007_remove_comment_order_alter_comment_shipper'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ships.order'),
        ),
    ]