# Generated by Django 3.2.16 on 2024-08-16 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial_squashed_0002_auto_20240626_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, help_text='Загрузите изображение для публикации.', null=True, upload_to='posts/', verbose_name='Изображение'),
        ),
    ]
