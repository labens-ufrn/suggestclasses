# Generated by Django 3.1.3 on 2020-11-13 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0083_vinculodocentesugestao'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquete',
            name='qtd_discentes_ativos',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]