# Generated by Django 4.1.4 on 2023-07-26 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_alter_member_email_alter_member_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='role',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
