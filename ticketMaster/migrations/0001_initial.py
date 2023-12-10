# Generated by Django 4.2.7 on 2023-12-05 20:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(max_length=20, unique=True)),
                ('eventName', models.CharField(max_length=200)),
                ('localDateTime', models.DateTimeField()),
                ('venue', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('imageLink', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SavedEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketMaster.event')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starRating', models.IntegerField(default=-1, editable=False)),
                ('comment', models.CharField(max_length=2000)),
                ('eventID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketMaster.event')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
