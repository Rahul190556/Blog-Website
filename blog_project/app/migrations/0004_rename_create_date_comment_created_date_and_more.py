# Generated by Django 4.2.1 on 2023-06-09 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_rename_created_date_comment_create_date"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="Create_date",
            new_name="created_date",
        ),
        migrations.RenameField(
            model_name="post",
            old_name="Create_date",
            new_name="created_date",
        ),
    ]