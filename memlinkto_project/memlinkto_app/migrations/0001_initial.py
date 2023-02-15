# Generated by Django 4.1.6 on 2023-02-15 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_email_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrlMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_url', models.CharField(max_length=1000)),
                ('long_url', models.CharField(max_length=10000)),
                ('email_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.emailaddress')),
            ],
        ),
    ]
