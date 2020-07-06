import aiohttp
from aiohttp import web
import argparse
import asyncio
import uuid


async def hello(request):
    return web.Response(text="Hello")

async def websocket_handler(request):
    client_list = []
    params = request.rel_url.query
    clientId = params['client_id']
    if client_id is None:
        exit
    else:
        client_list.append(clientId)
        print('Client Id: "%s" connected' % clientId)

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    sessions_list = []
    sessionId = str(uuid.uuid4())
    await ws.send_str(sessionId)
    sessions_list.append(sessionId)

  

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            print('ws message recived "%s"' % msg.data)

            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.PING:
            print('ping received')

        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws

def sessions(session):
    sessions = []
    return sessions

def main():
    app = web.Application()
    app.add_routes([web.get('/ws', websocket_handler)])
    web.run_app(app)

if __name__ == '__main__':
    main()
