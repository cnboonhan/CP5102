import os
import json
import sys
import logging
from proxy import Proxy, sleep_loop

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=LOGLEVEL)


if __name__ == '__main__':
    with Proxy(['--port', '8889', '--hostname', '0.0.0.0']):
        sleep_loop()
