# Moving Average Computing for Binance Streams

Сервис подписывается на [стримы Binance минутных свечей криптовалютных пар](https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams) и выводит в лог значения скользящего среднего.

По умолчанию слушаются следующие криптовалютные пары:
- BTC/USDT
- ETH/USDT
- BNB/BTC

Значения считаются по цене закрытия минутного периода в момент начала нового периода

## Params
Параметры сервиса описаны в файле ```params.json```:

- ```protocol``` - протокол, по которому необходимо производить подключение; по умолчанию - "wss"
- ```hostname``` - имя хоста; по умолчанию - "stream.binance.com"
- ```port``` - порт хоста; по умолчанию - 9443
- ```URL_path``` - путь к Веб-сокетам на хосте; по умолчанию - "/ws/"
- ```stream_names``` - имена стримов, на которые необходимо подписаться; по умолчанию - \["btcusdt@kline_1m", "ethusdt@kline_1m", "bnbbtc@kline_1m"]
- ```window_size``` - размер окна для вычисления скользящего среднего; по умолчанию - 3

Если вы собираете Docker-контейнер, то параметры необходимо указать в файле непосредственно перед его сбором



## Test
Для запуска тестов с помощью скриптов воспользуйтесь следующим набором команд
```
cd ./BinanceMovingAvg
pip install -r ./requirements.txt
python -m unittest discover -s Tests -p 'Test*.py'
```

Если вы используете Docker, воспользуйтесь следующим набором команд для сбора и запуска тестовой версии контейнера
```
cd ./BinanceMovingAvg
docker build --no-cache -t binance-ws-test-img --target test .
docker run -t --rm --name binance-ws-test binance-ws-test-img
```

После прохождения всех тестов контейнер прекращает свою работу



## Service running
Для запуска сервиса с помощью скриптов воспользуйтесь следующим набором команд
```
cd ./BinanceMovingAvg
pip install -r ./requirements.txt
python python ./Main.py
```

Если вы используете Docker, воспользуйтесь следующим набором команд для сбора и запуска сервиса
```
cd ./BinanceMovingAvg
docker build --no-cache -t binance-ws-prod-img --target production .
docker run -t --rm --name binance-ws-production binance-ws-prod-img
```

После запуска начинают логироваться значения скользящего среднего для криптовалютных пар

Для остановки работы сервиса воспользуйтесь сочетанием клавиш ```Ctrl+C```



## Logging
В ходе выполнения работы сервиса будут выводится логи

Если было получено количество значений меньшее необходимого для вычисления бегущего среднего, то будет выведена следующая информация:
```
2021-12-16 22:36:57,398 - [INFO] - BTCUSDT - 3 value(-s) to start computing moving avg...
...
2021-12-16 22:37:02,341 - [INFO] - BTCUSDT - 2 value(-s) to start computing moving avg...
... 
2021-12-16 22:38:02,313 - [INFO] - BTCUSDT - 1 value(-s) to start computing moving avg...
...
```

Начиная с момента получения достаточного количества значений для вычисления бегущего среднего, будет выводиться следующая информация:
```
2021-12-16 22:39:02,225 - [INFO] - BTCUSDT - 2021-12-16 19:38:59 - 47832.566667
...
2021-12-16 22:40:02,744 - [INFO] - BTCUSDT - 2021-12-16 19:39:59 - 47867.853333
... 
2021-12-16 22:41:02,343 - [INFO] - BTCUSDT - 2021-12-16 19:40:59 - 47896.256667
...
```
