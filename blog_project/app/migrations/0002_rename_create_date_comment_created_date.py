# Generated by Django 4.2.1 on 2023-06-07 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="Create_date",
            new_name="created_date",
        ),
    ]