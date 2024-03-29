# Generated by Django 3.1.7 on 2022-07-25 13:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CipherProdu# Generated by Django 3.1.7 on 2022-07-25 13:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CipherProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cipher_of_product', models.CharField(max_length=30, unique=True, verbose_name='Шифр изделия')),
                ('description_cipher_of_product', models.CharField(max_length=150, verbose_name='Расшифровка')),
            ],
            options={
                'verbose_name': 'Шифр изделия',
                'verbose_name_plural': 'Шифры изделия',
                'ordering': ['cipher_of_product'],
            },
        ),
        migrations.CreateModel(
            name='CorrectionDesignDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateField(verbose_name='Дата введения')),
                ('note_dd', models.CharField(blank=True, max_length=150, null=True, verbose_name='Примечание')),
                ('version_of_dd', models.PositiveIntegerField(default=0, editable=False, verbose_name='Порядковый номер коррекции')),
            ],
            options={
                'verbose_name': 'Коррекция КД',
                'verbose_name_plural': 'Коррекции КД',
                'ordering': ['id_design_document', 'version_of_dd'],
            },
        ),
        migrations.CreateModel(
            name='FormatDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_format', models.CharField(max_length=30, unique=True, verbose_name='Шифр формата')),
            ],
            options={
                'verbose_name': 'Формат документа',
                'verbose_name_plural': 'Форматы документа',
                'ordering': ['name_format'],
            },
        ),
        migrations.CreateModel(
            name='PrefixDecimalNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_prefix', models.CharField(max_length=20, unique=True, verbose_name='Код организации')),
                ('note_prefix_of_decimal_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Примечание')),
            ],
            options={
                'verbose_name': 'Код организации',
                'verbose_name_plural': 'Коды организации',
                'ordering': ['name_of_prefix'],
            },
        ),
        migrations.CreateModel(
            name='StatusOfDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_status_document', models.CharField(max_length=50, unique=True, verbose_name='Название статуса документа')),
                ('color_status_document', models.CharField(max_length=50, unique=True, verbose_name='Цвет надписи')),
            ],
            options={
                'verbose_name': 'Статус документа',
                'verbose_name_plural': 'Статусы документа',
                'ordering': ['name_status_document'],
            },
        ),
        migrations.CreateModel(
            name='TypeDesignDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cipher_of_type_document', models.CharField(blank=True, default='', max_length=50, verbose_name='Шифр документа')),
                ('name_of_type_document', models.CharField(max_length=150, unique=True, verbose_name='Наименование документа')),
                ('description_of_type_document', models.CharField(blank=True, max_length=150, null=True, verbose_name='Описание документа')),
                ('numb_order', models.CharField(blank=True, default='', max_length=10, verbose_name='Порядок сортировки')),
            ],
            options={
                'verbose_name': 'Тип документа',
                'verbose_name_plural': 'Типы документа',
                'ordering': ['cipher_of_type_document', '-numb_order'],
            },
        ),
        migrations.CreateModel(
            name='TypeOfFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cipher_of_type_file', models.CharField(max_length=50, unique=True, verbose_name='Шифр типа файла')),
                ('description_of_type_file', models.CharField(blank=True, max_length=150, null=True, verbose_name='Описание')),
                ('extension_file', models.CharField(max_length=20, verbose_name='Разширение файла')),
            ],
            options={
                'verbose_name': 'Тип файла документа',
                'verbose_name_plural': 'Типы файла документа',
                'ordering': ['cipher_of_type_file'],
            },
        ),
        migrations.CreateModel(
            name='FileDesignDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_of_document', models.FileField(upload_to='design_document/static/design_document/file_of_dd', verbose_name='Загрузите файл')),
                ('id_correction', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='design_document.correctiondesigndocument', verbose_name='Децимальный номер')),
                ('id_type_file', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='design_document.typeoffile', verbose_name='Тип файла документа')),
            ],
            options={
                'verbose_name': 'Файл документа',
                'verbose_name_plural': 'Файлы документа',
                'ordering': ['id_correction', 'id_type_file'],
            },
        ),
        migrations.CreateModel(
            name='DesignDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decimal_number', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(regex='^(\\d{1}\\.\\d{3}\\.\\d{3})(\\-\\d{2})?$')], verbose_name='Децимальный номер')),
                ('name_dd', models.CharField(max_length=100, verbose_name='Название')),
                ('date_create', models.DateField(verbose_name='Дата создания')),
                ('amount_sheet_dd', models.PositiveIntegerField(verbose_name='Количество листов')),
                ('note_dd', models.CharField(blank=True, max_length=150, null=True, verbose_name='Примечание')),
                ('inventory_number_dd', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(regex='^(\\d+)(\\-\\d+)?$')], verbose_name='Инвентарный номер')),
                ('confirm_change', models.BooleanField(default=False, verbose_name='Подтвердить изменения')),
                ('id_cipher_product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='design_document.cipherproduct', verbose_name='Шифр изделия')),
                ('id_format_document', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='design_document.formatdocument', verbose_name='Формат документа')),
                ('id_prefix', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='design_document.prefixdecimalnumber', verbose_name='Код организации')),
                ('id_status_document', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='design_document.statusofdocument', verbose_name='Статус документа')),
                ('id_type_document', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='design_document.typedesigndocument', verbose_name='Тип документа')),
                ('id_user_work_with_doc', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name': 'Конструкторская документация',
                'verbose_name_plural': 'Конструкторская документация',
                'ordering': ['id_prefix', 'decimal_number', 'id_type_document'],
            },
        ),
        migrations.AddField(
            model_name='correctiondesigndocument',
            name='id_design_document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='design_document.designdocument', verbose_name='Децимальный номер'),
        ),
    ]
