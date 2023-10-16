# Generated by Django 4.2.6 on 2023-10-15 23:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500)),
                ('answer', models.TextField(max_length=700)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.IntegerField()),
                ('mark', models.PositiveIntegerField(choices=[(4, 2), (8, 3), (16, 4), (32, 5)], default=4)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='core.question')),
            ],
        ),
    ]