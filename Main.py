import asyncio

from Utils.IOUtils import read_params
from StreamAPI.Stream import BinanceStream



if __name__ == '__main__':
    # Чтение параметров
    params = read_params('./params.json')
    ioloop = asyncio.get_event_loop()
    tasks = []
    # Создание стрима для каждой криптовалютной пары
    for stream_name in params['stream_names']:
        url = f"{params['protocol']}://{params['hostname']}:{params['port']}{params['URL_path']}{stream_name}"
        stream = BinanceStream(url=url,
                               name=stream_name,
                               window_size=params['window_size'])
        tasks.append(ioloop.create_task(stream.stream()))
    # Прослушиваем стрим, пока пользователь не прервет работу
    ioloop.run_until_complete(asyncio.wait(tasks))
    ioloop.run_forever()
    
    