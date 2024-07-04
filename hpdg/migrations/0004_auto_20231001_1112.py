# Generated by Django 3.2.15 on 2023-10-01 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hpdg', '0003_auto_20230930_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bv',
            name='creation_date',
            field=models.IntegerField(auto_created=True, default=1696155148),
        ),
        migrations.AlterField(
            model_name='commune',
            name='creation_date',
            field=models.IntegerField(auto_created=True, default=1696155148),
        ),
        migrations.AlterField(
            model_name='departement',
            name='creation_date',
            field=models.IntegerField(auto_created=True, default=1696155148),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='creation_date',
            field=models.IntegerField(auto_created=True, default=1696155148),
        ),
        migrations.AlterField(
            model_name='info',
            name='creation_date',
            field=models.IntegerField(auto_created=True, default=1696155148),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='creation_date',
            field=models.IntegerField(auto_created=True, default=1696155148),
        ),
        migrations.AlterField(
            model_name='message',
            name='creation_date',
            field=models.IntegerField(auto_created=True, default=1696155148),
        ),
        migrations.AlterField(
            model_name='pays',
            name='creation_date',
            field=models.IntegerField(auto_created=True, default=1696155148),
        ),
        migrations.AlterField(
            model_name='preinscription',
            name='creation_date',
            field=models.IntegerField(auto_created=True, default=1696155148),
        ),
        migrations.AlterField(
            model_name='region',
            name='creation_date',
            field=models.IntegerField(auto_created=True, default=1696155148),
        ),
        migrations.AlterField(
            model_name='user',
            name='creation_date',
            field=models.IntegerField(auto_created=True, default=1696155148),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_naissance',
            field=models.IntegerField(default=0),
        ),
    ]