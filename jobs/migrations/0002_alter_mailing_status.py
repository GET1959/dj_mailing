# Generated by Django 5.0.3 on 2024-03-26 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='status',
            field=models.CharField(default='created', max_length=150, verbose_name='статус рассылки'),
        ),
    ]
