import asyncio
import random
import ssl
import json
import time
import uuid

import aiohttp
from aiohttp_socks import ProxyConnector
from loguru import logger


async def connect_to_wss(user_id):
    device_id = str(uuid.uuid4())
    logger.info(device_id)

    # Configura il proxy SOCKS4
    proxy_host = "203.22.223.47"  # Sostituisci con l'indirizzo del proxy
    proxy_port = 80          # Sostituisci con la porta del proxy

    # Configura il connettore per il proxy SOCKS4
    connector = ProxyConnector.from_url(f'http://{proxy_host}:{proxy_port}')

    # Crea una sessione aiohttp con il proxy
    async with aiohttp.ClientSession(connector=connector) as session:
        uri = "wss://proxy.wynd.network:4650/"
        custom_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

        async with session.ws_connect(uri, ssl=False, headers=custom_headers) as websocket:
            async def send_ping():
                while True:
                    send_message = json.dumps(
                        {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}})
                    logger.debug(send_message)
                    await websocket.send_str(send_message)
                    await asyncio.sleep(20)

            await asyncio.sleep(1)
            asyncio.create_task(send_ping())

            while True:
                response = await websocket.receive()
                message = json.loads(response.data)
                logger.info(message)
                if message.get("action") == "AUTH":
                    auth_response = {
                        "id": message["id"],
                        "origin_action": "AUTH",
                        "result": {
                            "browser_id": device_id,
                            "user_id": user_id,
                            "user_agent": custom_headers['User-Agent'],
                            "timestamp": int(time.time()),
                            "device_type": "extension",
                            "version": "2.5.0"
                        }
                    }
                    logger.debug(auth_response)
                    await websocket.send_str(json.dumps(auth_response))

                elif message.get("action") == "PONG":
                    pong_response = {"id": message["id"], "origin_action": "PONG"}
                    logger.debug(pong_response)
                    await websocket.send_str(json.dumps(pong_response))


async def main():
    # TODO modifica user_id
    _user_id = '2oPB5YVo6djbpjlBojSobiwvUvi'
    await connect_to_wss(_user_id)


if __name__ == '__main__':
    asyncio.run(main())
