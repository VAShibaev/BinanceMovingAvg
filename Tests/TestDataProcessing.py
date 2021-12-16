import json
from datetime import datetime
import unittest

from StreamAPI.Stream import BinanceStream


'''
Unit-тест для прослушивания и обработки сообщений стрима
'''
class TestDataProcessing(unittest.TestCase):
    stream = BinanceStream('ws://localhost:4000', 'teststream', 3)
    
    # Проверка корректности работы функции получения имени валютной пары
    def test_1(self):
        data = {
            'k': {
                'T': 1639359479999,
                's': 'BNBBTC',
                'c': 5
            }
        }
        data_dict = data['k']
        pair_name = self.stream.get_pair_name(data_dict)
        self.assertEqual(pair_name, 'BNBBTC')


    # Проверка корректности работы функции получения времени закрытия
    def test_2(self):
        data = {
            'k': {
                'T': 1639359479999,
                's': 'BNBBTC',
                'c': 5
            }
        }
        data_dict = data['k']
        real_time_str = str(datetime.utcfromtimestamp(data_dict['T'] // 1000))
        time = self.stream.get_time(data_dict)
        self.assertEqual(time, real_time_str)


    # Проверка корректности работы функции добавления значений в список
    # при первом полученном сообщении
    def test_3(self):
        self.stream.values = []
        data = {
            'k': {
                'T': 1639359479999,
                's': 'BNBBTC',
                'c': 1.0
            }
        }
        data_dict = data['k']
        pair_name = self.stream.get_pair_name(data_dict)
        time = self.stream.get_time(data_dict)
        self.stream.update_values(data_dict, time, pair_name)
        self.assertEqual(self.stream.values, [1.0])

    # Проверка корректности работы функции добавления значений в список
    # при начале нового периода
    def test_4(self):
        self.stream.values = [1.0]
        self.stream.last_time = '2021-12-13 01:50:59'
        data = {
            'k': {
                'T': 1639360319999,
                's': 'BNBBTC',
                'c': 2.0
            }
        }
        data_dict = data['k']
        pair_name = self.stream.get_pair_name(data_dict)
        time = self.stream.get_time(data_dict)
        self.stream.update_values(data_dict, time, pair_name)
        self.assertEqual(self.stream.values, [1.0, 2.0])
        self.assertEqual(self.stream.last_time, '2021-12-13 01:51:59')

    # Проверка корректности работы функции обновления значений в спсике
    # при получении нового сообщения для данного периода
    def test_5(self):
        self.stream.values = [1.0, 2.0]
        self.stream.last_time = '2021-12-13 01:50:59'
        data = {
            'k': {
                'T': 1639360259999,
                's': 'BNBBTC',
                'c': 3.0
            }
        }
        data_dict = data['k']
        pair_name = self.stream.get_pair_name(data_dict)
        time = self.stream.get_time(data_dict)
        self.stream.update_values(data_dict, time, pair_name)
        self.assertEqual(self.stream.values, [1.0, 3.0])

    # Проверка корректности работы функции вычисления бегущего среднего
    def test_6(self):
        self.stream.values = [1.0, 2.0, 3.0]
        self.stream.last_time = '2021-12-13 01:50:59'
        data = {
            'k': {
                'T': 1639360319999,
                's': 'BNBBTC',
                'c': 4.0
            }
        }
        data_dict = data['k']
        pair_name = self.stream.get_pair_name(data_dict)
        time = self.stream.get_time(data_dict)
        self.stream.update_values(data_dict, time, pair_name)
        movinng_avg = self.stream.get_moving_avg(time)
        self.assertEqual(movinng_avg, 2.0)

    # Проверка корректности работы функции вычисления бегущего среднего
    # Когда в списке еще недостаточно значений для его вычисления
    def test_7(self):
        self.stream.values = [1.0, 2.0]
        self.stream.last_time = '2021-12-13 01:50:59'
        data = {
            'k': {
                'T': 1639360259999,
                's': 'BNBBTC',
                'c': 3.0
            }
        }
        data_dict = data['k']
        pair_name = self.stream.get_pair_name(data_dict)
        time = self.stream.get_time(data_dict)
        self.stream.update_values(data_dict, time, pair_name)
        movinng_avg = self.stream.get_moving_avg(time)
        self.assertEqual(movinng_avg, None)

    # Проверка корректности работы функции обработки сообщений стрима
    # при первом полученном сообщении
    def test_8(self):
        self.stream.values = []
        self.stream.last_time = None
        data = {
            'k': {
                'T': 1639360259999,
                's': 'BNBBTC',
                'c': 1.0
            }
        }
        data = json.dumps(data)
        self.stream.message_process(data)
        self.assertEqual(self.stream.values, [1.0])
        self.assertEqual(self.stream.last_time, '2021-12-13 01:50:59')

    # Проверка корректности работы функции обработки сообщений стрима
    # при получении сообщения, когда в списке достаточно значений для вычисления бегущего среднего
    def test_9(self):
        self.stream.values = [1.0, 2.0, 3.0]
        self.stream.last_time = '2021-12-13 01:50:59'
        data = {
            'k': {
                'T': 1639360319999,
                's': 'BNBBTC',
                'c': 4.0
            }
        }
        data = json.dumps(data)
        self.stream.message_process(data)
        self.assertEqual(self.stream.values, [2.0, 3.0, 4.0])
        self.assertEqual(self.stream.last_time, '2021-12-13 01:51:59')


if __name__ == "__main__":
    unittest.main()