# Generated by Django 4.0.4 on 2022-05-10 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ships', '0014_remove_rating_creator_remove_rating_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipper',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, related_name='shippers', to='ships.tag'),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('rate', models.PositiveSmallIntegerField(default=0)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ships.order')),
                ('shipper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ships.shipper')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'Like'), (1, 'Dislike'), (2, 'Love')], default=0)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ships.order')),
                ('shipper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ships.shipper')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
