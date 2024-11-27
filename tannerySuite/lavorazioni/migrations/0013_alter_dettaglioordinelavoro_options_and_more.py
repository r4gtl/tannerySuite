# Generated by Django 4.2.16 on 2024-11-27 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lavorazioni', '0012_dettaglioordinelavoro_descrizione'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dettaglioordinelavoro',
            options={'ordering': ['numero_riga']},
        ),
        migrations.AddField(
            model_name='dettaglioordinelavoro',
            name='numero_riga',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]