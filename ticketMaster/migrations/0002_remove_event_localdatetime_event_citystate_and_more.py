# Generated by Django 4.2.7 on 2023-12-05 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketMaster', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='localDateTime',
        ),
        migrations.AddField(
            model_name='event',
            name='cityState',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='eventLink',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='localDate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='localTime',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='eventName',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='imageLink',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='venue',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
