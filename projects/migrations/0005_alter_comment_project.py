# Generated by Django 3.2.9 on 2021-12-09 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_comment_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='project',
            field=models.CharField(default=None, max_length=128, null=True),
        ),
    ]
