# Generated by Django 3.0.5 on 2020-04-22 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0058_auto_20200421_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sugestaoturma',
            name='horarios',
            field=models.ManyToManyField(related_name='sugestoes', to='core.Horario'),
        ),
    ]
