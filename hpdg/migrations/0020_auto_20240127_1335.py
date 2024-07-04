# Generated by Django 3.2.15 on 2024-01-27 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hpdg', '0019_auto_20240127_1242'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='info',
            options={'ordering': ['-creation_date']},
        ),
        migrations.AlterField(
            model_name='bv',
            name='creation_date',
            field=models.IntegerField(default=1706362517),
        ),
        migrations.AlterField(
            model_name='bv',
            name='last_modified',
            field=models.IntegerField(default=1706362517),
        ),
        migrations.AlterField(
            model_name='commune',
            name='creation_date',
            field=models.IntegerField(default=1706362517),
        ),
        migrations.AlterField(
            model_name='departement',
            name='creation_date',
            field=models.IntegerField(default=1706362517),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='creation_date',
            field=models.IntegerField(default=1706362517),
        ),
        migrations.AlterField(
            model_name='info',
            name='creation_date',
            field=models.IntegerField(default=1706362517),
        ),
        migrations.AlterField(
            model_name='info',
            name='time',
            field=models.IntegerField(default=1706362517),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='creation_date',
            field=models.IntegerField(default=1706362517),
        ),
        migrations.AlterField(
            model_name='message',
            name='creation_date',
            field=models.IntegerField(default=1706362517),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_envoi',
            field=models.IntegerField(default=1706362517),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_modif',
            field=models.IntegerField(default=1706362517),
        ),
        migrations.AlterField(
            model_name='pays',
            name='creation_date',
            field=models.IntegerField(default=1706362517),
        ),
        migrations.AlterField(
            model_name='preinscription',
            name='creation_date',
            field=models.IntegerField(default=1706362517),
        ),
        migrations.AlterField(
            model_name='region',
            name='creation_date',
            field=models.IntegerField(default=1706362517),
        ),
        migrations.AlterField(
            model_name='token',
            name='creation_date',
            field=models.IntegerField(default=1706362517),
        ),
        migrations.AlterField(
            model_name='token',
            name='end_time',
            field=models.IntegerField(default=1708954517),
        ),
        migrations.AlterField(
            model_name='user',
            name='creation_date',
            field=models.IntegerField(default=1706362517),
        ),
    ]