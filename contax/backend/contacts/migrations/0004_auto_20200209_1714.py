# Generated by Django 2.2.10 on 2020-02-09 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("contacts", "0003_auto_20200209_1710")]

    operations = [
        migrations.AlterField(
            model_name="postaladdress",
            name="state",
            field=models.CharField(blank=True, max_length=200, null=True),
        )
    ]
