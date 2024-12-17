# Generated by Django 2.1.5 on 2024-12-05 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_project_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('submitted', 'Submitted')], default='draft', max_length=10),
        ),
    ]