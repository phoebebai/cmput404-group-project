# Generated by Django 3.0.2 on 2020-02-01 04:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('bio', models.TextField()),
                ('host', models.URLField()),
                ('first_name', models.CharField(max_length=256)),
                ('last_name', models.CharField(max_length=256)),
                ('display_name', models.CharField(max_length=256)),
                ('url', models.URLField()),
                ('github', models.URLField()),
            ],
        ),
    ]
