# Generated by Django 2.2.10 on 2021-11-24 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_answers"),
    ]

    operations = [
        migrations.CreateModel(
            name="Users",
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
                ("firstname", models.CharField(max_length=20)),
                ("lastname", models.CharField(max_length=20)),
                ("password", models.CharField(max_length=20)),
            ],
            options={
                "unique_together": {("firstname", "lastname")},
            },
        ),
    ]
