# Generated by Django 2.0.1 on 2018-01-15 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0002_auto_20180115_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='due_date',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bills.Service'),
        ),
    ]
