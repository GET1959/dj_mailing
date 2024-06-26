# Generated by Django 5.0.3 on 2024-05-03 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="article",
            options={
                "permissions": [("set_activity", "Управление статьей")],
                "verbose_name": "статья",
                "verbose_name_plural": "статьи",
            },
        ),
        migrations.AddField(
            model_name="article",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="активна"),
        ),
    ]
