# Generated by Django 5.0.3 on 2024-05-14 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0008_alter_mailing_options_alter_mailing_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="frequency",
            field=models.CharField(
                choices=[
                    ("10 секунд", "10 секунд"),
                    ("минута", "минута"),
                    ("день", "день"),
                    ("неделя", "неделя"),
                    ("месяц", "месяц"),
                ],
                max_length=50,
                verbose_name="периодичность рассылки",
            ),
        ),
        migrations.AlterField(
            model_name="mailing",
            name="is_active",
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name="активна"),
        ),
    ]
