# Generated by Django 2.1.5 on 2024-10-15 01:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='images',
        ),
        migrations.AlterField(
            model_name='project',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
        migrations.AddField(
            model_name='projectimage',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='projects.Project'),
        ),
        migrations.AddField(
            model_name='project',
            name='project_images',
            field=models.ManyToManyField(blank=True, related_name='projects', to='projects.ProjectImage'),
        ),
    ]
