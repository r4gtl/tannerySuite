# Generated by Django 4.2.16 on 2024-11-24 12:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('acquistopelli', '0004_alter_concia_descrizione_alter_quality_descrizione_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DettaglioLotto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pezzi', models.IntegerField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dettaglio_lotto', to=settings.AUTH_USER_MODEL)),
                ('fk_concia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dettaglio_lotto', to='acquistopelli.concia')),
                ('fk_lotto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acquistopelli.lotto')),
                ('fk_quality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dettaglio_lotto', to='acquistopelli.quality')),
                ('fk_sezione', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dettaglio_lotto', to='acquistopelli.sezione')),
                ('fk_spessore', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dettaglio_lotto', to='acquistopelli.spessore')),
                ('fk_taglio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dettaglio_lotto', to='acquistopelli.taglio')),
                ('fk_tipoanimale', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dettaglio_lotto', to='acquistopelli.tipoanimale')),
            ],
        ),
    ]