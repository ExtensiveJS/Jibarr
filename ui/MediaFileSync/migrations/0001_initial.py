# Generated by Django 2.1.1 on 2018-10-12 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('media_id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_source', models.CharField(max_length=200)),
                ('media_source_id', models.IntegerField()),
                ('media_lastUpd', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('profile_id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_name', models.CharField(max_length=200)),
                ('profile_lastUpd', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ProfileMedia',
            fields=[
                ('profilemedia_id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_id', models.IntegerField()),
                ('media_id', models.IntegerField()),
            ],
        ),
    ]
