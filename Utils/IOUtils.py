import json

'''
Чтение json-файла с параметрами
params_file_path - путь до файла
На выходе - словарь с параметрами {имя_парамтера: значение_параметра}
Если какой-то параметр отсутствует или тип значения не соответствует ожидаемому, возникает IOError
'''
def read_params(params_file_path: str) -> dict:
    # Чтение файла
    with open(params_file_path) as fin:
        content = fin.read()
    # Преобразование строки в словарь
    data_dict = json.loads(content)
    # Проверка параметров и их типов
    if 'protocol' not in data_dict or not isinstance(data_dict['protocol'], str) or \
        'hostname' not in data_dict or not isinstance(data_dict['hostname'], str) or \
        'port' not in data_dict or not isinstance(data_dict['port'], int) or \
        'URL_path' not in data_dict or not isinstance(data_dict['URL_path'], str) or  \
        'stream_names' not in data_dict or not isinstance(data_dict['stream_names'], list) or \
        'window_size' not in data_dict or not isinstance(data_dict['window_size'], int):
        raise IOError
    return data_dict
    
    