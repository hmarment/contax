# Generated by Django 2.2.10 on 2020-02-15 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contacts", "0004_auto_20200209_1714"),
    ]

    operations = [
        migrations.RemoveField(model_name="postaladdress", name="contact",),
        migrations.RemoveField(model_name="postaladdress", name="name",),
        migrations.CreateModel(
            name="PostalAddressContact",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                (
                    "contact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contacts.Contact",
                    ),
                ),
                (
                    "postal_address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contacts.PostalAddress",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="postaladdress",
            name="contacts",
            field=models.ManyToManyField(
                blank=True,
                related_name="postal_addresses",
                through="contacts.PostalAddressContact",
                to="contacts.Contact",
            ),
        ),
    ]
