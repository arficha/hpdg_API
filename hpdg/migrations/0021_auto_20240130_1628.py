# Generated by Django 3.2.15 on 2024-01-30 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hpdg', '0020_auto_20240127_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bv',
            name='creation_date',
            field=models.IntegerField(default=1706632112),
        ),
        migrations.AlterField(
            model_name='bv',
            name='last_modified',
            field=models.IntegerField(default=1706632112),
        ),
        migrations.AlterField(
            model_name='commune',
            name='creation_date',
            field=models.IntegerField(default=1706632112),
        ),
        migrations.AlterField(
            model_name='departement',
            name='creation_date',
            field=models.IntegerField(default=1706632112),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='creation_date',
            field=models.IntegerField(default=1706632112),
        ),
        migrations.AlterField(
            model_name='info',
            name='creation_date',
            field=models.IntegerField(default=1706632112),
        ),
        migrations.AlterField(
            model_name='info',
            name='time',
            field=models.IntegerField(default=1706632112),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='creation_date',
            field=models.IntegerField(default=1706632112),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='email',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='id',
            field=models.CharField(max_length=200, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='nom',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='photo',
            field=models.CharField(default='none', max_length=1000),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='prenom',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='sexe',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='statut',
            field=models.CharField(default='1', max_length=1000),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='sympathisant',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='message',
            name='creation_date',
            field=models.IntegerField(default=1706632112),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_envoi',
            field=models.IntegerField(default=1706632112),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_modif',
            field=models.IntegerField(default=1706632112),
        ),
        migrations.AlterField(
            model_name='pays',
            name='creation_date',
            field=models.IntegerField(default=1706632112),
        ),
        migrations.AlterField(
            model_name='preinscription',
            name='creation_date',
            field=models.IntegerField(default=1706632112),
        ),
        migrations.AlterField(
            model_name='region',
            name='creation_date',
            field=models.IntegerField(default=1706632112),
        ),
        migrations.AlterField(
            model_name='token',
            name='creation_date',
            field=models.IntegerField(default=1706632112),
        ),
        migrations.AlterField(
            model_name='token',
            name='end_time',
            field=models.IntegerField(default=1709224112),
        ),
        migrations.AlterField(
            model_name='user',
            name='creation_date',
            field=models.IntegerField(default=1706632112),
        ),
    ]