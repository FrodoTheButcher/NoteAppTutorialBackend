# Generated by Django 4.2.5 on 2023-09-18 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("UsersAPP", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="points",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
