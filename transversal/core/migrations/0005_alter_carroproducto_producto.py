# Generated by Django 3.2.5 on 2021-07-20 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210720_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carroproducto',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.producto', unique=True),
        ),
    ]