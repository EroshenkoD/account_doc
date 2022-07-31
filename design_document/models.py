import os
from django.db import models
from django.db.models import Max
from django.core.validators import RegexValidator
from django.contrib.auth.import os
from django.db import models
from django.db.models import Max
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.exceptions import NON_FIELD_ERRORS


class FormatDocument(models.Model):
    name_format = models.CharField('Шифр формата', max_length=30, unique=True)

    def __str__(self):
        return self.name_format

    class Meta:
        verbose_name = 'Формат документа'
        verbose_name_plural = 'Форматы документа'
        ordering = ['name_format']


class StatusOfDocument(models.Model):
    name_status_document = models.CharField('Название статуса документа', max_length=50, unique=True)
    color_status_document = models.CharField('Цвет надписи', max_length=50, unique=True)

    def __str__(self):
        return self.name_status_document

    class Meta:
        verbose_name = 'Статус документа'
        verbose_name_plural = 'Статусы документа'
        ordering = ['name_status_document']


class PrefixDecimalNumber(models.Model):
    name_of_prefix = models.CharField('Код организации', max_length=20, unique=True)
    note_prefix_of_decimal_number = models.CharField('Примечание', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name_of_prefix

    class Meta:
        verbose_name = 'Код организации'
        verbose_name_plural = 'Коды организации'
        ordering = ['name_of_prefix']


class CipherProduct(models.Model):
    cipher_of_product = models.CharField('Шифр изделия', max_length=30, unique=True)
    description_cipher_of_product = models.CharField('Расшифровка', max_length=150)

    def __str__(self):
        return self.cipher_of_product

    class Meta:
        verbose_name = 'Шифр изделия'
        verbose_name_plural = 'Шифры изделия'
        ordering = ['cipher_of_product']


class TypeOfFile(models.Model):
    cipher_of_type_file = models.CharField('Шифр типа файла', max_length=50, unique=True)
    description_of_type_file = models.CharField('Описание', max_length=150, blank=True, null=True)
    extension_file = models.CharField('Разширение файла', max_length=20)

    def __str__(self):
        return self.cipher_of_type_file

    class Meta:
        verbose_name = 'Тип файла документа'
        verbose_name_plural = 'Типы файла документа'
        ordering = ['cipher_of_type_file']


class TypeDesignDocument(models.Model):
    cipher_of_type_document = models.CharField('Шифр документа', max_length=50, blank=True, default='')
    name_of_type_document = models.CharField('Наименование документа', max_length=150, unique=True)
    description_of_type_document = models.CharField('Описание документа', max_length=150, blank=True, null=True)
    numb_order = models.CharField('Порядок сортировки', max_length=10, blank=True, default='')

    def __str__(self):
        return self.name_of_type_document

    class Meta:
        verbose_name = 'Тип документа'
        verbose_name_plural = 'Типы документа'
        ordering = ['cipher_of_type_document', '-numb_order']


class DesignDocument(models.Model):
    id_cipher_product = models.ForeignKey(CipherProduct, on_delete=models.PROTECT, verbose_name='Шифр изделия')
    id_prefix = models.ForeignKey(PrefixDecimalNumber, on_delete=models.PROTECT, verbose_name='Код организации')
    decimal_number = models.CharField('Децимальный номер', max_length=30,
                                      validators=[RegexValidator(regex=r'^(\d{1}\.\d{3}\.\d{3})(\-\d{2})?$')])
    id_type_document = models.ForeignKey(TypeDesignDocument, on_delete=models.PROTECT, verbose_name='Тип документа')
    name_dd = models.CharField('Название', max_length=100)
    date_create = models.DateField('Дата создания')
    id_format_document = models.ForeignKey(FormatDocument, on_delete=models.PROTECT, verbose_name='Формат документа')
    amount_sheet_dd = models.PositiveIntegerField('Количество листов')
    note_dd = models.CharField('Примечание', max_length=150, blank=True, null=True)
    inventory_number_dd = models.CharField('Инвентарный номер', max_length=10,
                                           validators=[RegexValidator(regex=r'^(\d+)(\-\d+)?$')])
    id_status_document = models.ForeignKey(StatusOfDocument, on_delete=models.PROTECT, verbose_name='Статус документа')
    id_user_work_with_doc = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Сотрудник')
    confirm_change = models.BooleanField(verbose_name='Подтвердить изменения', default=False)

    def save(self, *args, **kwargs):
        super(DesignDocument, self).save(*args, **kwargs)
        check_version = CorrectionDesignDocument.objects.filter(
            id_design_document_id=self.id).aggregate(version=Max('version_of_dd'))['version']
        if check_version is None:
            version = CorrectionDesignDocument(id_design_document_id=self.id, date_create=self.date_create)
            version.save()

    def clean(self):

        if not self.confirm_change:
            check_d_n = DesignDocument.objects.filter(decimal_number=self.decimal_number,
                                                      id_prefix_id=PrefixDecimalNumber.objects.get(
                                                          name_of_prefix=self.id_prefix).id,
                                                      id_type_document=TypeDesignDocument.objects.get(
                                                          name_of_type_document=self.id_type_document).id
                                                      ).exists()
            if check_d_n:
                messages_err = DesignDocument.objects.get(decimal_number=self.decimal_number,
                                                          id_prefix_id=PrefixDecimalNumber.objects.get(
                                                              name_of_prefix=self.id_prefix).id,
                                                          id_type_document=TypeDesignDocument.objects.get(
                                                              name_of_type_document=self.id_type_document).id
                                                          ).__str__()
                raise ValidationError({
                    'id_prefix': [
                        ValidationError(
                            message="Дециальные номер {} уже существует".format(messages_err),
                        )
                    ]
                })

            if self.inventory_number_dd != '0':
                inventory_number_check = DesignDocument.objects.filter(
                    inventory_number_dd=self.inventory_number_dd).exists()
                if inventory_number_check:
                    messages_err = DesignDocument.objects.get(inventory_number_dd=self.inventory_number_dd).__str__()
                    raise ValidationError({
                        'inventory_number_dd': [
                            ValidationError(
                                message="Инвентарный номер {} уже присвоен документу {}".format(
                                    self.inventory_number_dd, messages_err),
                            )
                        ]
                    })
        self.confirm_change = False
        super(DesignDocument, self).clean()

    def __str__(self):
        return '{} {} {}'.format(PrefixDecimalNumber.objects.get(id=self.id_prefix_id), self.decimal_number,
                                 TypeDesignDocument.objects.get(id=self.id_type_document_id).cipher_of_type_document)

    class Meta:
        verbose_name = 'Конструкторская документация'
        verbose_name_plural = 'Конструкторская документация'
        ordering = ['id_prefix', 'decimal_number', 'id_type_document']


class CorrectionDesignDocument(models.Model):
    id_design_document = models.ForeignKey(DesignDocument, on_delete=models.PROTECT, verbose_name='Децимальный номер')
    date_create = models.DateField('Дата введения')
    note_dd = models.CharField('Примечание', max_length=150, blank=True, null=True)
    version_of_dd = models.PositiveIntegerField('Порядковый номер коррекции', editable=False, default=0)

    def clean(self):
        check_date_correction = CorrectionDesignDocument.objects.filter(id_design_document=self.id_design_document,
                                                                        date_create=self.date_create).exists()
        if check_date_correction:
            err_mess = DesignDocument.objects.get(id=CorrectionDesignDocument.objects.get(
                id_design_document=self.id_design_document,
                date_create=self.date_create).id_design_document_id).__str__()
            raise ValidationError({
                'date_create': [
                    ValidationError(
                        message="Коррекция для {} на {} уже существует".format(err_mess,
                                                                               self.date_create.strftime('%d.%m.%y')),
                    )
                ]
            })

        super(CorrectionDesignDocument, self).clean()

    def save(self, *args, **kwargs):
        max_version_now = CorrectionDesignDocument.objects.filter(
            id_design_document_id=self.id_design_document_id).aggregate(
            max_version=Max('version_of_dd'))['max_version']
        if max_version_now is None:
            self.version_of_dd = 0
        else:
            self.version_of_dd = max_version_now + 1
        super(CorrectionDesignDocument, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Коррекция КД'
        verbose_name_plural = 'Коррекции КД'
        ordering = ['id_design_document', 'version_of_dd']

    def __str__(self):
        text_corr = ', без коррекции'
        if self.version_of_dd != 0:
            text_corr = ', корр. от {}'.format(self.date_create.strftime('%d.%m.%y'))
        return '{}{}'.format(DesignDocument.objects.get(id=self.id_design_document_id).__str__(), text_corr)


class FileDesignDocument(models.Model):
    id_correction = models.ForeignKey(CorrectionDesignDocument, on_delete=models.PROTECT,
                                      verbose_name='Децимальный номер')
    id_type_file = models.ForeignKey(TypeOfFile, on_delete=models.PROTECT, verbose_name='Тип файла документа')
    file_of_document = models.FileField(upload_to='design_document/static/design_document/file_of_dd',
                                        verbose_name='Загрузите файл')

    def clean(self):
        check_file = FileDesignDocument.objects.filter(id_correction_id=self.id_correction_id,
                                                       id_type_file_id=self.id_type_file_id).exists()
        if check_file:
            raise ValidationError({
                'id_type_file': [
                    ValidationError(
                        message="Для данной коррекции, файл с таким расширением, уже был загружен!",
                    )
                ]
            })

        extension_file = TypeOfFile.objects.get(id=self.id_type_file_id).extension_file
        if extension_file != os.path.splitext(self.file_of_document.name)[1]:
            raise ValidationError({
                'id_type_file': [
                    ValidationError(
                        message="Не соответствует расширение файла",
                    )
                ]
            })
        super(FileDesignDocument, self).clean()

    def save(self, *args, **kwargs):
        ext = os.path.splitext(self.file_of_document.name)[1]

        new_name = '{}\{}v{}{}'.format(CipherProduct.objects.get(id=DesignDocument.objects.get(
            id=CorrectionDesignDocument.objects.get(
                id=self.id_correction_id).id_design_document_id).id_cipher_product_id).cipher_of_product,
                                       DesignDocument.objects.get(id=CorrectionDesignDocument.objects.get(
                                           id=self.id_correction_id).id_design_document_id).__str__(),
                                       CorrectionDesignDocument.objects.get(id=self.id_correction_id).version_of_dd,
                                       ext)

        self.file_of_document.name = new_name
        super(FileDesignDocument, self).save(*args, **kwargs)

    def __str__(self):
        return '{}, тип файла {}'.format(CorrectionDesignDocument.objects.get(id=self.id_correction_id).__str__(),
                                         TypeOfFile.objects.get(id=self.id_type_file_id).__str__())

    class Meta:
        verbose_name = 'Файл документа'
        verbose_name_plural = 'Файлы документа'
        ordering = ['id_correction', 'id_type_file']
