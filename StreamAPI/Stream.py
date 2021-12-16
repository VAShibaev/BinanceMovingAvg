import json
import logging
import websockets
from datetime import datetime

from Utils.MathUtils import moving_average

'''
    Класс для стрима, прослушивающего с помощью Веб-сокетов Binance и выводящего в логи скользящее среднее
'''
class BinanceStream:
    
    '''
        Конструктор класса
        url - URL-адрес Веб-сокета дляподписки на стрим
        name - название стрима
        window_size - размер окна для вычисления скользящего среднего
    '''
    def __init__(self, url: str, name: str, window_size: int):
        self.url = url
        self.name = name
        self.windows_size = window_size
        
        self.values = []            # История значений цены закрытия
        self.last_time = None       # Время закрытия текущего периода
        
        # Логер для вывода результатов
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - [%(levelname)s] - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    '''
        Подписка на стрим
        Стрим слушается до тех пор, пока пользователь не прервет его работу
    '''
    async def stream(self) -> None:
        # Слушаем до тех пор, пока пользователь не прервет работу
        while True:
            try:
                # Подписываемся на стрим
                async with websockets.connect(self.url) as websocket:
                    # Слушаем его до тех пор, пока он отправляет сообщения
                    async for message in websocket:
                        # Для каждого отправленного сообщения производим его обработку
                        self.message_process(message)
            # Если в ходе работы стрима возникла ошибка
            # Выводим сообщение об этом
            # И пытаемся переподписаться на стрим
            except Exception:
                self.logger.error(f'Stream {self.name} error...')
                self.logger.error(f'Trying reconnect...')

    '''
        Получение имени валютной пары
        data_dict - словарь, пришедший сообщением с Binance
    '''
    def get_pair_name(self, data_dict: dict) -> str:
        return data_dict['s']

    '''
        Получение времени
        data_dict - словарь, пришедший сообщением с Binance
    '''
    def get_time(self, data_dict: dict) -> str:
        # Время приходит в миллисекундах, по этому преобразуем его в секунды и преобразуем к формату дата-время
        return str(datetime.utcfromtimestamp(data_dict['T'] // 1000))

    '''
        Вычисление скользящего среднего
        time - время текущей цены закрытия периода
    '''
    def get_moving_avg(self, time: str) -> float:
        result = None
        # Если текущая цена закрфтия периода не совпадает с предыдущей,
        # то это означает, что начался новый период
        if self.last_time != time:
            # Проверяем, достаточно ли значений в списке для вычисления скользящего среднего
            # Поскольку значения в списке обновляются до вычисления среднего,
            # то мы должны не учитывать последний элемент в списке
            if len(self.values) == self.windows_size + 1:
                # Считаем скользящее среднее
                moving_avg = moving_average(self.values[:-1])
                # Если подсчет завершился без ошибки, сохраняем значение
                if moving_avg != -1:
                    result = moving_avg
        return result

    '''
        Обновление текущего состояния
        data_dict - словарь, пришедший сообщением с Binance
        time - время текущей цены закрытия периода
        pair_name - имя валютной пары
    '''
    def update_values(self, data_dict: dict, time: str, pair_name: str) -> None:
        # Берем текущую цену закрытия из полученного сообщения
        close_price = float(data_dict['c'])
        # Если время закрытия периода для полученного сообщения совпадает с сохраненным временем,
        # перезаписываем сохраненную цену закрытия для данного периода
        if self.last_time == time:
            self.values[-1] = close_price
        # Если время закрытия периода для полученного сообщения не совпадает с сохраненным временем,
        # это означает, что начался новый период
        else:
            # Добавляем в список цену закрытия
            self.values.append(close_price)
            # Если в списке еще недостаточно значений для вычисления бегущего среднего
            if len(self.values) != self.windows_size + 1:
                # Выводим информацию об этом
                self.logger.info(
                    f"{pair_name:7} - {self.windows_size - len(self.values) + 1} value(-s) to start computing moving avg...")
                # Перезаписываем время закрытия
                self.last_time = time

    '''
        Обработка сообщения, полученного из стрима Binance
        message - тело ответа
    '''
    def message_process(self, message: str) -> None:
        # Преобразуем ответ с Binance в словарь
        data_dict = json.loads(message)['k']
        # Находим имя валютной пары
        pair_name = self.get_pair_name(data_dict)
        # Находим время закрытия текущего периода
        time = self.get_time(data_dict)
        # Обновляем значения в списке цен закрытия и время закрытия
        self.update_values(data_dict, time, pair_name)
        # Вычисляем скользящее среднее
        moving_avg = self.get_moving_avg(time)
        # Если скользящее среднее было вычислено
        if moving_avg:
            # Выводим информацию о текущем значении скользящего среднего
            self.logging(pair_name, self.last_time, moving_avg)
            # Обновляем время на время закрытия начавшегося периода
            self.last_time = time
            # Убираем из списка значения самый старый элемент
            self.values.pop(0)

    '''
        Вывод информации о скользящем среднем
        name - имя валютной пары
        time - время закрытия, на момент которого считается скользящее среднее
        moving_avg - значение скользящего среднего
    '''
    def logging(self, name: str, time: str, moving_avg: float) -> None:
        self.logger.info(f"{name:7} - {time} - {moving_avg:.6f}")