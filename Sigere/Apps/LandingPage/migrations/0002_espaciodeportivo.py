# Generated by Django 5.1.6 on 2025-04-02 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LandingPage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EspacioDeportivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('tipo_espacio', models.CharField(choices=[('cancha', 'Cancha'), ('gimnasio', 'Gimnasio'), ('piscina', 'Piscina'), ('otro', 'Otro')], max_length=20)),
                ('deporte', models.CharField(max_length=50)),
                ('ubicacion', models.CharField(max_length=150)),
                ('tiene_suplementos', models.BooleanField(default=False)),
                ('descripcion', models.TextField(blank=True)),
                ('imagen_url', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
