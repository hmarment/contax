# Generated by Django 2.2.10 on 2020-02-09 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("contacts", "0001_initial")]

    operations = [
        migrations.RemoveField(model_name="postaladdress", name="contacts"),
        migrations.AlterModelOptions(name="contact", options={"ordering": ["created"]}),
        migrations.DeleteModel(name="PhoneNumber"),
        migrations.DeleteModel(name="PostalAddress"),
    ]
