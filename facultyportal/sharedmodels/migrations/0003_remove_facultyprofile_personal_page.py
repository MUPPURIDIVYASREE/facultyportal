# Generated by Django 5.2.3 on 2025-06-19 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharedmodels', '0002_alter_guidance_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facultyprofile',
            name='personal_page',
        ),
    ]
