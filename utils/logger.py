"""Logger"""
import logging
import websockets

class SingletonType(type):
    """Singleton for logger and send logger to websocket"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(object, metaclass=SingletonType):
    """Logger"""
    instance_socket = None
    def __init__(self):
        self._logger = logging.getLogger("crumbs")
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s \t [%(levelname)s] > %(message)s')

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self._logger.addHandler(stream_handler)

    async def logger(self, message):
        self._logger.info(message)
        try:
            await self.send_message_to_app(message)
        except:
            pass

    async def send_message_to_app(self, message):
        uri = "ws://localhost:11234"
        try:
            async with websockets.connect(uri) as websocket:
                await websocket.send(message)
        except:
            pass