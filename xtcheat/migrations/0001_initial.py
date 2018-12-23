# Generated by Django 2.1.3 on 2018-12-02 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=11)),
                ('phoneon', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254)),
                ('emailon', models.BooleanField(default=False)),
            ],
        ),
    ]