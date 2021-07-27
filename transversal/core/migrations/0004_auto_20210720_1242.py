# Generated by Django 3.2.5 on 2021-07-20 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_producto_actualizacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='carro',
            name='activo',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='carro',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='producto',
            name='actualizacion',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]