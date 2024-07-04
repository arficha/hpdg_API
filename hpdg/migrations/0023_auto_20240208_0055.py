# Generated by Django 3.2.15 on 2024-02-08 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hpdg', '0022_auto_20240208_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='photo',
            field=models.CharField(default='none', max_length=1000),
        ),
        migrations.AlterField(
            model_name='bv',
            name='creation_date',
            field=models.IntegerField(default=1707353748),
        ),
        migrations.AlterField(
            model_name='bv',
            name='last_modified',
            field=models.IntegerField(default=1707353748),
        ),
        migrations.AlterField(
            model_name='commune',
            name='creation_date',
            field=models.IntegerField(default=1707353748),
        ),
        migrations.AlterField(
            model_name='departement',
            name='creation_date',
            field=models.IntegerField(default=1707353748),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='creation_date',
            field=models.IntegerField(default=1707353748),
        ),
        migrations.AlterField(
            model_name='info',
            name='creation_date',
            field=models.IntegerField(default=1707353748),
        ),
        migrations.AlterField(
            model_name='info',
            name='time',
            field=models.IntegerField(default=1707353748),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='creation_date',
            field=models.IntegerField(default=1707353748),
        ),
        migrations.AlterField(
            model_name='message',
            name='creation_date',
            field=models.IntegerField(default=1707353748),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_envoi',
            field=models.IntegerField(default=1707353748),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_modif',
            field=models.IntegerField(default=1707353748),
        ),
        migrations.AlterField(
            model_name='pays',
            name='creation_date',
            field=models.IntegerField(default=1707353748),
        ),
        migrations.AlterField(
            model_name='preinscription',
            name='creation_date',
            field=models.IntegerField(default=1707353748),
        ),
        migrations.AlterField(
            model_name='region',
            name='creation_date',
            field=models.IntegerField(default=1707353748),
        ),
        migrations.AlterField(
            model_name='token',
            name='creation_date',
            field=models.IntegerField(default=1707353748),
        ),
        migrations.AlterField(
            model_name='token',
            name='end_time',
            field=models.IntegerField(default=1709945748),
        ),
        migrations.AlterField(
            model_name='user',
            name='creation_date',
            field=models.IntegerField(default=1707353748),
        ),
    ]
