import chardet
import csv
import json
import re
import yaml

"""1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку
определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый
«отчетный» файл в формате CSV. Для этого:"""
"""a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с
данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно получиться четыре
списка — например, os_prod_list, os_name_list, os_code_list, os_type_list.
В этой же функции создать главный список для хранения данных отчета — например, main_data
— и поместить в него названия столбцов отчета в виде списка: «Изготовитель
системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих 
столбцов также оформить в виде списка и поместить в файл main_data (также для
каждого файла);"""


def get_data(lst):
    lists, os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], [], []
    lists.extend([os_prod_list, os_name_list, os_code_list, os_type_list])
    main_data = []
    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data.append(headers)

    for file in lst:
        with open(file, 'rb') as f:
            content_bytes = f.read()
            data = content_bytes.decode(chardet.detect(content_bytes)['encoding'])

        os_prod_reg = re.compile(r'Изготовитель системы:\s*\S*')
        os_prod_list.append(os_prod_reg.findall(data)[0].split()[2])

        os_name_reg = re.compile(r'Название ОС:\s*\S*')
        os_name_list.append(os_name_reg.findall(data)[0].split()[2])

        os_code_reg = re.compile(r'Код продукта:\s*\S*')
        os_code_list.append(os_code_reg.findall(data)[0].split()[2])

        os_type_reg = re.compile(r'Тип системы:\s*\S*')
        os_type_list.append(os_type_reg.findall(data)[0].split()[2])

    for i in range(len(lists[0])):
        new_list = []
        for lst in lists:
            new_list.append(lst[i])
        main_data.append(new_list)

    # print(f"{main_data=}")
    return main_data


files_list = ['info_1.txt', 'info_2.txt', 'info_3.txt']
get_data(files_list)

"""b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой
функции реализовать получение данных через вызов функции get_data(), а также
сохранение подготовленных данных в соответствующий CSV-файл;"""


def write_to_csv(file, files_lst):
    with open(file, 'w', encoding='utf-8', newline='') as f_l:
        data = get_data(files_lst)
        f_writer = csv.writer(f_l, quoting=csv.QUOTE_MINIMAL)
        # ,lineterminator='\n') второй вариант убрать пустые строки
        f_writer.writerows(data)

    with open(file, 'r', encoding='utf-8') as f:
        print(f.read())


"""c. Проверить работу программы через вызов функции write_to_csv()."""

write_to_csv('report_file.csv', files_list)

"""2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с
информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными. Для
этого:"""
"""a. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар
(item), количество (quantity), цена (price), покупатель (buyer), дата (date). Функция
должна предусматривать запись данных в виде словаря в файл orders.json. При
записи данных указать величину отступа в 4 пробельных символа;"""


def write_order_to_json(item, quantity, price, buyer, date):
    new_dict = {'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date}
    with open('orders.json', 'r', encoding='utf-8') as file:
        file_content = json.load(file)
        file_content['orders'].append(new_dict)

    with open('orders.json', 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)


"""b. Проверить работу программы через вызов функции write_order_to_json() с передачей
в нее значений каждого параметра."""

write_order_to_json('PC', 1, 12.80, 'Ivan', '03.10.2022')
write_order_to_json('Radio', 3, 15.70, 'Semen', '05.10.2022')
write_order_to_json('Мафон', 5, 18.50, 'Толян', '05.10.2022')

with open('orders.json', 'r', encoding='utf-8') as f:
    content = json.load(f)
    # print(content)

"""3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий
сохранение данных в файле YAML-формата. Для этого:"""

"""a. Подготовить данные для записи в виде словаря, в котором первому ключу
соответствует список, второму — целое число, третьему — вложенный словарь, где
значение каждого ключа — это целое число с юникод-символом, отсутствующим в
кодировке ASCII (например, €);"""

my_dict = {
    'items': ['computer', 'printer', 'keyboard', 'mouse'],
    'item_quantity': 1,
    'item_price': {
        'computer': '200€-1000€',
        'printer': '100€-300€',
        'keyboard': '5€-50€',
        'mouse': '4€-7€'}
}

"""b. Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а
также установить возможность работы с юникодом: allow_unicode = True;"""

with open('file.yaml', 'w', encoding='utf-8') as fl:
    yaml.dump(my_dict, fl, default_flow_style=False, allow_unicode=True, sort_keys=False)

"""c. Реализовать считывание данных из созданного файла и проверить, совпадают ли они
с исходными."""

with open('file.yaml', 'r', encoding='utf-8') as fl:
    f_content = yaml.load(fl, yaml.SafeLoader)
    print(f_content)

print(my_dict == f_content)
