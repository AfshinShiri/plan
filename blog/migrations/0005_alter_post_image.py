# Generated by Django 3.2.4 on 2021-06-03 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='../static/img/default.jpg', upload_to=''),
        ),
    ]
