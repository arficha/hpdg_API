# Generated by Django 3.2.15 on 2024-02-14 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hpdg', '0027_auto_20240214_0146'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentaire',
            name='replyTo',
            field=models.CharField(default='none', max_length=10000),
        ),
        migrations.AlterField(
            model_name='bv',
            name='creation_date',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='bv',
            name='last_modified',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='commentaire',
            name='creation_date',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='commentaire',
            name='time',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='commune',
            name='creation_date',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='departement',
            name='creation_date',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='creation_date',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='info',
            name='creation_date',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='info',
            name='image',
            field=models.CharField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='info',
            name='time',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='creation_date',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='message',
            name='creation_date',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_envoi',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_modif',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='pays',
            name='creation_date',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='preinscription',
            name='creation_date',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='reaction',
            name='creation_date',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='reaction',
            name='time',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='region',
            name='creation_date',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='session',
            name='creation_date',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='session',
            name='end_time',
            field=models.IntegerField(default=1710530524),
        ),
        migrations.AlterField(
            model_name='token',
            name='creation_date',
            field=models.IntegerField(default=1707938524),
        ),
        migrations.AlterField(
            model_name='user',
            name='creation_date',
            field=models.IntegerField(default=1707938524),
        ),
    ]
