# Generated by Django 3.1.4 on 2021-03-05 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('desc', models.TextField(blank=True, verbose_name='description')),
                ('date', models.DateField()),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('comment', models.TextField(blank=True)),
                ('registered', models.DateTimeField(auto_now_add=True)),
                ('workshops', models.ManyToManyField(to='workshops.Workshop')),
            ],
            options={
                'ordering': ['first_name', 'last_name'],
            },
        ),
    ]
