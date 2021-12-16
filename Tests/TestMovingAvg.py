import unittest

from Utils.MathUtils import moving_average

'''
Unit-тест для функции вычисления бегущего среднего
'''
class TestMovingAvg(unittest.TestCase):
    # Случай, когда передан пустой словарь
    def test_1(self):
        self.assertEqual(moving_average([]), -1)

    # Случай равенства вычисленного значения ожидаемому для указанного списка
    def test_2(self):
        self.assertEqual(moving_average([1]), 1)

    # Случай равенства вычисленного значения ожидаемому для указанного списка
    def test_3(self):
        self.assertEqual(moving_average([1, 2]), 1.5)

    # Случай равенства вычисленного значения ожидаемому для указанного списка
    def test_4(self):
        self.assertEqual(moving_average([1, 2, 3]), 2)

    # Случай равенства вычисленного значения ожидаемому для указанного списка
    def test_5(self):
        self.assertEqual(moving_average([1.5, 1.5, 6.0]), 3.0)

    # Случай, когда передан не словарь
    def test_6(self):
        self.assertEqual(moving_average((1, 2, 3)), -1)

    # Случай, когда передан не словарь
    def test_7(self):
        self.assertEqual(moving_average({1, 2, 3}), -1)
        
if __name__ == "__main__":
    unittest.main()