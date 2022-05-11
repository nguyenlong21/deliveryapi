# Generated by Django 4.0.4 on 2022-05-05 15:57

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ships', '0003_tag_rename_subject_delivery_name_alter_category_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shipper',
            name='delivery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shippers', to='ships.delivery'),
        ),
        migrations.AlterField(
            model_name='shipper',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shipper',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, related_name='shippers', to='ships.tag'),
        ),
    ]