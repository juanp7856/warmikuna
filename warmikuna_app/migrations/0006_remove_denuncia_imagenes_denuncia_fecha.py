# Generated by Django 4.1.6 on 2023-04-19 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warmikuna_app', '0005_denuncia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='denuncia',
            name='imagenes',
        ),
        migrations.AddField(
            model_name='denuncia',
            name='fecha',
            field=models.DateField(null=True),
        ),
    ]