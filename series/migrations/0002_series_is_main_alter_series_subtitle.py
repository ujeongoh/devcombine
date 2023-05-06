# Generated by Django 4.2 on 2023-05-06 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("series", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="series",
            name="is_main",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="series",
            name="subtitle",
            field=models.CharField(max_length=300, null=True),
        ),
    ]
