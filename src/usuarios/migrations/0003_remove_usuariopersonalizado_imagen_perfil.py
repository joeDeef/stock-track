# Generated by Django 5.1.3 on 2024-11-30 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_usuariopersonalizado_imagen_perfil'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuariopersonalizado',
            name='imagen_perfil',
        ),
    ]
