# Generated by Django 4.1.6 on 2023-04-17 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warmikuna_app', '0003_alter_usuario_fnacim'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='apellido',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='dni',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='numero',
            field=models.CharField(max_length=9, null=True),
        ),
    ]