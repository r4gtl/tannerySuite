# Generated by Django 4.2.16 on 2024-11-27 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lavorazioni', '0010_unitamisura'),
    ]

    operations = [
        migrations.AddField(
            model_name='dettaglioordinelavoro',
            name='fk_unita_misura',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dettaglio_ordine_lavoro', to='lavorazioni.unitamisura'),
        ),
    ]
