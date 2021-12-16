import unittest
from json.decoder import JSONDecodeError

from Utils.IOUtils import read_params


'''
Unit-тест для функции чтения json-файла с параметрами
'''
class TestMovingAvg(unittest.TestCase):
    # Случай, когда файл с параметрами отсутствует
    def test_1(self):
        self.assertRaises(FileNotFoundError, read_params, './Tests/configs/abs.json')

    # Случай, когда файл с параметрами поврежден
    def test_2(self):
        self.assertRaises(JSONDecodeError, read_params, './Tests/configs/test_2.json')

    # Случай, когда один из необходимых параметров отсутствует
    def test_3(self):
        self.assertRaises(IOError, read_params, './Tests/configs/test_3.json')

    # Случай, когда тип одного из параметров не соответствует ожидаемому
    def test_4(self):
        self.assertRaises(IOError, read_params, './Tests/configs/test_4.json')

    # Случай завершения без ошибки
    def test_5(self):
        self.assertEqual(read_params('./Tests/configs/test_5.json'),
                         {
                             "protocol": "wss",
                             "hostname": "stream.binance.com",
                             "port": 9443,
                             "URL_path": "/ws/",
    
                             "stream_names": [
                                 "btcusdt@kline_1m"
                             ],
    
                             "window_size": 5
                         })


if __name__ == "__main__":
    unittest.main()