# Generated by Django 3.2.4 on 2021-06-06 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_post_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='file',
            field=models.FileField(null=True, upload_to='videos/', verbose_name='video'),
        ),
    ]
