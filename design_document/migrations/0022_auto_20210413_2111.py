# Generated by Django 3.1.7 on 2021-04-13 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design_document', '0021_auto_20210411_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filedesigndocument',
            name='file_of_document',
            field=models.FileField(upload_to='design_document/file_of_dd/', verbose_name='Загрузите файл'),
        ),
    ]
