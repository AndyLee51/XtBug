# Generated by Django 2.1.3 on 2018-12-12 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xtcheat', '0003_userinfo_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='remember',
            field=models.BooleanField(default=False),
        ),
    ]