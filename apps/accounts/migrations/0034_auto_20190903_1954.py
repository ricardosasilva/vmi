# Generated by Django 2.2.4 on 2019-09-03 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0033_auto_20190830_1756'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='member',
            new_name='members',
        ),
        migrations.AlterField(
            model_name='organization',
            name='subject',
            field=models.CharField(blank=True, db_index=True, default='644726315817694', help_text='Subject ID', max_length=64),
        ),
    ]
