# Generated by Django 2.1.1 on 2018-09-11 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CsvDoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('csv_file', models.FileField(upload_to='csv/%Y/%m/%d')),
            ],
        ),
    ]
