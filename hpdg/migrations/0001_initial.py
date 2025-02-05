# Generated by Django 3.2.15 on 2023-07-27 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Atelier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=100)),
                ('id_event', models.CharField(max_length=100)),
                ('categorie_atelier', models.CharField(choices=[('1', 'GLOBAL BUSINESS'), ('2', 'B2B/B2C '), ('3', 'FORMATION ET COACHING'), ('4', 'REFLEXIONS'), ('5', 'COCKTAILS ET NETWORKING'), ('6', 'B.LEAD HER'), ('7', 'G100'), ('8', 'CREATIF')], max_length=100)),
                ('libelle', models.CharField(max_length=70)),
                ('logo', models.CharField(max_length=10000000)),
                ('salle', models.CharField(max_length=100)),
                ('nb_placep', models.CharField(max_length=200)),
                ('nb_placev', models.CharField(max_length=200)),
                ('price', models.CharField(max_length=200)),
                ('meeting_url', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, default='', max_length=1000)),
                ('date_debut', models.DateTimeField()),
                ('date_fin', models.DateTimeField()),
                ('date_init', models.DateField(auto_now_add=True)),
                ('statut', models.CharField(choices=[('1', 'waiting_for_response'), ('2', 'acccepted'), ('3', 'rejected'), ('4', 'deleted'), ('5', 'suspended')], max_length=100)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['date_init'],
            },
        ),
    ]
