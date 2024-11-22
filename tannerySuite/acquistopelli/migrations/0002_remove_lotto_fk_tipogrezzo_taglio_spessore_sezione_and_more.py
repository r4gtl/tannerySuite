# Generated by Django 4.2.16 on 2024-11-22 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('acquistopelli', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lotto',
            name='fk_tipogrezzo',
        ),
        migrations.CreateModel(
            name='Taglio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrizione', models.CharField(max_length=50)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='taglio', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'tagli',
                'ordering': ['descrizione'],
            },
        ),
        migrations.CreateModel(
            name='Spessore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrizione', models.CharField(max_length=10)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='spessore', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'spessori',
                'ordering': ['descrizione'],
            },
        ),
        migrations.CreateModel(
            name='Sezione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrizione', models.CharField(max_length=10)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sezione', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'sezioni',
                'ordering': ['descrizione'],
            },
        ),
        migrations.CreateModel(
            name='Quality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrizione', models.CharField(max_length=10)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quality', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'qualities',
                'ordering': ['descrizione'],
            },
        ),
        migrations.CreateModel(
            name='Concia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrizione', models.CharField(max_length=10)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='concia', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'conce',
                'ordering': ['descrizione'],
            },
        ),
        migrations.AddField(
            model_name='lotto',
            name='fk_concia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lotto', to='acquistopelli.concia'),
        ),
        migrations.AddField(
            model_name='lotto',
            name='fk_quality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lotto', to='acquistopelli.quality'),
        ),
        migrations.AddField(
            model_name='lotto',
            name='fk_sezione',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lotto', to='acquistopelli.sezione'),
        ),
        migrations.AddField(
            model_name='lotto',
            name='fk_spessore',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lotto', to='acquistopelli.spessore'),
        ),
        migrations.AddField(
            model_name='lotto',
            name='fk_taglio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lotto', to='acquistopelli.taglio'),
        ),
    ]
