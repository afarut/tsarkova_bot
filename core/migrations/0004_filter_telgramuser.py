# Generated by Django 4.2.6 on 2023-10-28 06:20

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_question_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('questions', models.ManyToManyField(related_name='filters', to='core.question')),
            ],
        ),
        migrations.CreateModel(
            name='TelgramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.PositiveIntegerField()),
                ('selected_filter', models.ForeignKey(on_delete=models.SET(core.models.get_default_filter), to='core.filter')),
            ],
        ),
    ]
