# Generated by Django 4.2.16 on 2024-11-27 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lavorazioni', '0013_alter_dettaglioordinelavoro_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='portomateriale',
            old_name='decrizione_inglese',
            new_name='descrizione_inglese',
        ),
    ]