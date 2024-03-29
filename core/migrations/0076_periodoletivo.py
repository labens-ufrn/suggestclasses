# Generated by Django 3.0.6 on 2020-06-04 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0075_auto_20200531_1317'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeriodoLetivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('ano', models.IntegerField()),
                ('periodo', models.IntegerField()),
                ('data_inicio', models.DateField()),
                ('data_fim', models.DateField()),
                ('data_consolidacao', models.DateField()),
                ('status', models.CharField(choices=[('1', 'Consolidado'), ('2', 'Ativo'), ('3', 'Planejado'), ('4', 'Suspenso'), ('5', 'Cancelado')], max_length=1)),
                ('observacoes', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
