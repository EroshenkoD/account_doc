from django.shortcuts import render
from .models import CipherProduct
from .models import PrefixDecimalNumber
from .models import TypeDesignDocument
from .models import Dfrom django.shortcuts import render
from .models import CipherProduct
from .models import PrefixDecimalNumber
from .models import TypeDesignDocument
from .models import DesignDocument
from .models import FileDesignDocument
from .models import CorrectionDesignDocument
from django.db.models import Max, Min
from .models import StatusOfDocument
from .models import TypeOfFile


def look_dd(request):
    """Функция реализующая поиск и вывод документов только для просмотра, отображаеться только посленяя версия
    документа в формате файла ПДФ"""
    data = {'cipher_product': CipherProduct.objects.all(),
            'prefix_decimal_number': PrefixDecimalNumber.objects.all(),
            'type_design_document': TypeDesignDocument.objects.all()}
    if request.method == 'POST':
        design_document = DesignDocument.objects.all()
        """ Сортировка по шифру изделия"""
        try:
            cipher_product = CipherProduct.objects.get(cipher_of_product=request.POST.get("cipher_product"))
            design_document = design_document.filter(id_cipher_product_id=cipher_product.id)
        except Exception:
            cipher_product = None
        """ Сортировка по коду предприятия"""
        try:
            prefix_decimal_number = PrefixDecimalNumber.objects.get(
                name_of_prefix=request.POST.get("prefix_decimal_number"))
            design_document = design_document.filter(id_prefix_id=prefix_decimal_number.id)
        except Exception:
            prefix_decimal_number = None
        """ Поис по полному иил частичному цифровому обозначению в децимальном номере"""
        try:
            reg_kod = request.POST.get("reg_kod")
            design_document = design_document.filter(decimal_number__startswith=reg_kod)
            if reg_kod == '':
                reg_kod = None
        except Exception:
            reg_kod = None
        """ Сортировка по типу документа"""
        try:
            type_design_document = TypeDesignDocument.objects.get(
                name_of_type_document=request.POST.get("type_design_document"))
            design_document = design_document.filter(id_type_document_id=type_design_document.id)
        except Exception:
            type_design_document = None
        """ Если не задан ниодин из параметров, вывод информации не происходит"""
        if cipher_product is not None or prefix_decimal_number is not None or reg_kod is not None or \
                type_design_document is not None:
            data['list_link'] = {}
            """ Подготавливаем словарь данных для вывода, он должен состоять из словарей, 
            ключем которого является децимальный номер, а значением - список следующего формата: [Путь к файлу ПДФ, 
            Шифр изделия, название документа, [Статус документа, цвет в который красить выводимую информацию]]"""
            for obj in design_document:
                try:
                    data['list_link'][obj.__str__()] = [FileDesignDocument.objects.get(
                        id_correction_id=CorrectionDesignDocument.objects.filter(id_design_document_id=obj.id).order_by(
                            'version_of_dd').last().id, id_type_file_id=1).file_of_document,
                                                    CipherProduct.objects.get(
                                                        id=obj.id_cipher_product_id).cipher_of_product,
                                                    obj.name_dd,
                                                    StatusOfDocument.objects.filter(
                                                        id=obj.id_status_document_id).values('name_status_document',
                                                                                             'color_status_document')]
                except Exception:
                    continue

            if not data['list_link']:
                del data['list_link']
                data['err_mess'] = "Нет данных по указаным критериям поиска!"

    return render(request, 'design_document/look_dd.html', data)


def look_and_download_dd(request):
    """Функция реализующая поиск и вывод документов для просмотра и скачивания, с возмоностью отображать
    все версии и типы файлов"""
    data = {'cipher_product': CipherProduct.objects.all(),
            'prefix_decimal_number': PrefixDecimalNumber.objects.all(),
            'type_design_document': TypeDesignDocument.objects.all(),
            'type_file_document': TypeOfFile.objects.all()}
    if request.method == 'POST':
        design_document = DesignDocument.objects.all()
        """ Сортировка по шифру изделия"""
        try:
            cipher_product = CipherProduct.objects.get(cipher_of_product=request.POST.get("cipher_product"))
            design_document = design_document.filter(id_cipher_product_id=cipher_product.id)
        except Exception:
            cipher_product = None
        """ Сортировка по коду организации"""
        try:
            prefix_decimal_number = PrefixDecimalNumber.objects.get(
                name_of_prefix=request.POST.get("prefix_decimal_number"))
            design_document = design_document.filter(id_prefix_id=prefix_decimal_number.id)
        except Exception:
            prefix_decimal_number = None
        """ Поис по полному иил частичному цифровому обозначению в децимальном номере"""
        try:
            reg_kod = request.POST.get("reg_kod")
            design_document = design_document.filter(decimal_number__startswith=reg_kod)
            if reg_kod == '':
                reg_kod = None
        except Exception:
            reg_kod = None
        """ Сортировка по типу документа"""
        try:
            type_design_document = TypeDesignDocument.objects.get(
                name_of_type_document=request.POST.get("type_design_document"))
            design_document = design_document.filter(id_type_document_id=type_design_document.id)
        except Exception:
            type_design_document = None
        """ Проверка какой тип файла документа необходим, если его не находят в базе, значит надо все типы файлов"""
        try:
            type_file_design_document = TypeOfFile.objects.get(
                cipher_of_type_file=request.POST.get("type_file_design_document"))
        except Exception:
            type_file_design_document = None
        """ Если не задан ниодин из параметров : Шифр, Код органзации, цифровое обозначение децимального номера 
        или его часть,тип документа, то вывод информации не происходит"""
        if cipher_product is not None or prefix_decimal_number is not None or reg_kod is not None or \
                type_design_document is not None:
            """ В зависимости от запроса есть 4 варианта, когда надо все версии документа, но одного типа файла, 
            когда надо все типы файла но последней версии,
            когда надо все версии но одного типа файла, 
            когда надо один тип файла последней версии, все выполняестя по одному принципу, по отсортированым выше 
            требованием, формируються списки с данными, а потом формируется словарь для вывода нданных"""
            if request.POST.get("all_version") and type_file_design_document is None:
                all_obj_all_version = {}
                all_obj_all_format_file = {}
                """ Проходим по списку отсортированых документов и создаем словарь в котором ключ это айди документа, 
                а значение - все его версий"""
                for obj in design_document:
                    all_obj_all_version[obj.id] = CorrectionDesignDocument.objects.filter(
                        id_design_document_id=obj.id)
                """ Проходим по списку коррекций и создаем словарь, ге ключ - это айди, а значение - все его файлы"""
                for id_dd, list_obj_version in all_obj_all_version.items():
                    for obj_version in list_obj_version:
                        all_obj_all_format_file[obj_version.id] = FileDesignDocument.objects.filter(
                            id_correction_id=obj_version.id)
                """ Выполняем формирования словарря данных для вывода информации на странице браузера"""
                data['all_obj_all_version_all_format_file'] = []
                for id_dd, list_obj_corr in all_obj_all_version.items():
                    obj_design_document = DesignDocument.objects.get(id=id_dd)
                    cipher_product_dd = CipherProduct.objects.get(
                        id=obj_design_document.id_cipher_product_id).cipher_of_product
                    reg_numb_dd = obj_design_document.__str__()
                    status_dd = StatusOfDocument.objects.filter(id=obj_design_document.id_status_document_id).values(
                        'name_status_document', 'color_status_document')
                    for obj_corr in list_obj_corr:
                        if obj_corr.version_of_dd == 0:
                            text_corr = 'Без коррекции'
                        else:
                            text_corr = 'Корр. от {}'.format(obj_corr.date_create.strftime('%d.%m.%y'))

                        for obj_file_dd in all_obj_all_format_file[obj_corr.id]:
                            type_file = TypeOfFile.objects.get(id=obj_file_dd.id_type_file_id)
                            if type_file.id == 1:
                                only_look = True
                            else:
                                only_look = False
                            try:
                                temp = [only_look,
                                        reg_numb_dd,
                                        text_corr,
                                        str(obj_file_dd.file_of_document),
                                        cipher_product_dd,
                                        obj_design_document.name_dd,
                                        status_dd,
                                        type_file.cipher_of_type_file]
                            except Exception:
                                continue
                            data['all_obj_all_version_all_format_file'].append(temp)

                if not data['all_obj_all_version_all_format_file']:
                    del data['all_obj_all_version_all_format_file']
                    data['err_mess'] = "Нет данных по указаным критериям поиска!"
            elif request.POST.get("all_version"):
                all_obj_all_version = {}
                for obj in design_document:
                    all_obj_all_version[obj.id] = CorrectionDesignDocument.objects.filter(id_design_document_id=obj.id)

                data['all_obj_all_version'] = []
                if type_file_design_document.id == 1:
                    only_look = True
                else:
                    only_look = False

                for key, value in all_obj_all_version.items():
                    obj_design_document = DesignDocument.objects.get(id=key)
                    cipher_product_dd = CipherProduct.objects.get(
                        id=obj_design_document.id_cipher_product_id).cipher_of_product
                    reg_numb_dd = obj_design_document.__str__()
                    status_dd = StatusOfDocument.objects.filter(id=obj_design_document.id_status_document_id).values(
                        'name_status_document', 'color_status_document')
                    for obj in value:
                        if obj.version_of_dd == 0:
                            text_corr = 'Без коррекции'
                        else:
                            text_corr = 'Корр. от {}'.format(obj.date_create.strftime('%d.%m.%y'))
                        try:
                            temp = [only_look,
                                    reg_numb_dd,
                                    text_corr,
                                    str(FileDesignDocument.objects.get(id_correction_id=obj.id,
                                                                   id_type_file=
                                                                   type_file_design_document).file_of_document),
                                    cipher_product_dd,
                                    obj_design_document.name_dd,
                                    status_dd,
                                    type_file_design_document.cipher_of_type_file]
                        except Exception:
                            continue
                        data['all_obj_all_version'].append(temp)

                if not data['all_obj_all_version']:
                    del data['all_obj_all_version']
                    data['err_mess'] = "Нет данных по указаным критериям поиска!"

            elif type_file_design_document is None:
                all_obj_all_format_file = {}
                for obj in design_document:
                    all_obj_all_format_file[obj.id] = FileDesignDocument.objects.filter(
                        id_correction_id=CorrectionDesignDocument.objects.filter(id_design_document_id=obj.id).order_by(
                            'version_of_dd').last().id)

                data['all_obj_all_format_file'] = []
                for key, value in all_obj_all_format_file.items():
                    obj_design_document = DesignDocument.objects.get(id=key)
                    cipher_product_dd = CipherProduct.objects.get(
                        id=obj_design_document.id_cipher_product_id).cipher_of_product
                    reg_numb_dd = obj_design_document.__str__()
                    status_dd = StatusOfDocument.objects.filter(id=obj_design_document.id_status_document_id).values(
                        'name_status_document', 'color_status_document')
                    for obj in value:
                        if obj.id_type_file_id == 1:
                            only_look = True
                        else:
                            only_look = False

                        version_corr = CorrectionDesignDocument.objects.get(id=obj.id_correction_id)
                        if version_corr.version_of_dd == 0:
                            text_corr = 'Без коррекции'
                        else:
                            text_corr = 'Корр. от {}'.format(version_corr.date_create.strftime('%d.%m.%y'))
                        temp = [only_look,
                                reg_numb_dd,
                                TypeOfFile.objects.get(id=obj.id_type_file_id).cipher_of_type_file,
                                str(obj.file_of_document),
                                cipher_product_dd,
                                obj_design_document.name_dd,
                                status_dd,
                                text_corr]
                        data['all_obj_all_format_file'].append(temp)

                if not data['all_obj_all_format_file']:
                    del data['all_obj_all_format_file']
                    data['err_mess'] = "Нет данных по указаным критериям поиска!"

            else:
                all_obj = design_document
                data['all_obj'] = {}
                for obj in all_obj:
                    try:
                        obj_file_dd = FileDesignDocument.objects.get(id_correction_id=
                                                                     CorrectionDesignDocument.objects.
                                                                     filter(id_design_document_id=obj.id).order_by(
                                                                         'version_of_dd').last().id,
                                                                     id_type_file_id=type_file_design_document.id)
                        version_corr = CorrectionDesignDocument.objects.get(id=obj_file_dd.id_correction_id)
                        if version_corr.version_of_dd == 0:
                            text_corr = 'Без коррекции'
                        else:
                            text_corr = 'Корр. от {}'.format(version_corr.date_create.strftime('%d.%m.%y'))

                        data['all_obj'][obj.__str__()] = [str(obj_file_dd.file_of_document),
                                                          CipherProduct.objects.get(
                                                            id=obj.id_cipher_product_id).cipher_of_product,
                                                          obj.name_dd,
                                                          StatusOfDocument.objects.filter(id=
                                                                                          obj.id_status_document_id).
                                                              values('name_status_document', 'color_status_document'),
                                                          text_corr,
                                                          TypeOfFile.objects.get(id=obj_file_dd.id_type_file_id).
                                                              cipher_of_type_file]
                    except Exception:
                        continue

                if not data['all_obj']:
                    del data['all_obj']
                    data['err_mess'] = "Нет данных по указаным критериям поиска!"

    return render(request, 'design_document/look_and_download_dd.html', data)
