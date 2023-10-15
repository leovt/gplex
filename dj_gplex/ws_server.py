import asyncio
from collections import defaultdict
import json

import django
import websockets

from django.core.signing import TimestampSigner
from django.contrib.auth import get_user_model
from django.core.signing import SignatureExpired, BadSignature

django.setup()

User = get_user_model()

connections = defaultdict(set)

def get_user(token):
    try:
        signer = TimestampSigner()
        username = signer.unsign(token, max_age=100)
        return User.objects.get(username=username)
    except (BadSignature, SignatureExpired, User.DoesNotExist):
        return None

async def handler(websocket):
    token = await websocket.recv()
    user = await asyncio.to_thread(get_user, token)
    if user is None:
        await websocket.close(1011, "authentication failed")
        return
    connections[user.username].add(websocket)

    try:
        async for message in websocket:
            try:
                event = json.loads(message)
                if event['type'] == 'chat':
                    # TODO: validate the fields, especially 'from'
                    receivers = connections[event['to']] | connections[event['from']]
                    websockets.broadcast(receivers, message)
            except Exception:
                pass
    finally:
        connections[user.username].discard(websocket)
        if not connections[user.username]:
            del connections[user.username]


async def main():
    async with websockets.serve(handler, "localhost", 8888):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
