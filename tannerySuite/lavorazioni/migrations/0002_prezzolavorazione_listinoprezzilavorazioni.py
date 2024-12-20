# Generated by Django 4.2.16 on 2024-11-24 14:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('anagrafiche', '0002_fornitore_fornitorelavorazioniesterne_and_more'),
        ('lavorazioni', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrezzoLavorazione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inserimento', models.DateField(default=datetime.date.today)),
                ('prezzo', models.DecimalField(decimal_places=3, max_digits=8)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prezzi_lavorazioni', to=settings.AUTH_USER_MODEL)),
                ('fk_lavorazione', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prezzo', to='lavorazioni.lavorazione')),
            ],
            options={
                'ordering': ['-data_inserimento'],
            },
        ),
        migrations.CreateModel(
            name='ListinoPrezziLavorazioni',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listino_prezzi_lavorazioni', to=settings.AUTH_USER_MODEL)),
                ('fk_fornitorelavorazioniesterne', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listino_prezzi_lavorazioni', to='anagrafiche.fornitorelavorazioniesterne')),
                ('fk_lavorazione', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listino_prezzi_lavorazioni', to='lavorazioni.lavorazione')),
            ],
            options={
                'ordering': ['fk_lavorazione__descrizione'],
            },
        ),
    ]
