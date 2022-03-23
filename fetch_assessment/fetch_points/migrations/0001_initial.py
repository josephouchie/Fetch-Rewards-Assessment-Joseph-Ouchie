# Generated by Django 3.2.12 on 2022-03-23 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payer', models.CharField(max_length=50)),
                ('points', models.IntegerField()),
                ('timestamp', models.CharField(max_length=20)),
            ],
        ),
    ]
