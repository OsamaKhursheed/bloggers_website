# Generated by Django 4.1.7 on 2023-12-02 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shared_app', '0003_delete_b1log'),
        ('blogger', '0003_blog_makessdsr'),
    ]

    operations = [
        migrations.DeleteModel(
            name='blog_makessdsr',
        ),
    ]
