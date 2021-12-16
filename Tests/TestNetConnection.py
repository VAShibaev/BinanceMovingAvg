import json
import unittest
import asyncio
import websockets

from Utils.IOUtils import read_params

'''
Unit-тест для проверки возможности прослушивания указанных стримов
'''
class TestDataProcessing(unittest.TestCase):
    
    async def stream(self, url: str, stream_name: str) -> None:
        async with websockets.connect(url) as websocket:
            message = await websocket.recv()
            data_dict = json.loads(message)
            self.assertIn('k', data_dict)
            self.assertIn('s', data_dict['k'])
            self.assertIn('T', data_dict['k'])
            self.assertIn('c', data_dict['k'])
            
            stream_name = stream_name.split('@')[0]
            self.assertEqual(data_dict['k']['s'].lower(), stream_name)

    
    def test_1(self):
        params = read_params('./params.json')
        ioloop = asyncio.get_event_loop()
        tasks = []
        for stream_name in params['stream_names']:
            url = f"{params['protocol']}://{params['hostname']}:{params['port']}{params['URL_path']}{stream_name}"
            tasks.append(ioloop.create_task(self.stream(url, stream_name)))
        ioloop.run_until_complete(asyncio.wait(tasks))