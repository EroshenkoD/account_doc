# Generated by Django 3.1.7 on 2021-03-30 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('design_document', '0004_auto_20210330_2156'),
    ]

    operations = [
        migrations.RenameField(
            model_name='designdocument',
            old_name='Шифр документа',
            new_name='Тип документа',
        ),
    ]
