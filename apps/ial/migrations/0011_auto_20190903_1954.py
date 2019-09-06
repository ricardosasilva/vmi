# Generated by Django 2.2.4 on 2019-09-03 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ial', '0010_auto_20190806_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identityassuranceleveldocumentation',
            name='evidence_subclassification',
            field=models.CharField(blank=True, choices=[('DRIVERS-LICENSE', "Driver's License"), ('MEDICAID-CARD', 'Medicaid card'), ('MEDICARE-CARD', 'Medicare card'), ('I9', 'I-9 Employee verification')], default='', max_length=256),
        ),
    ]
