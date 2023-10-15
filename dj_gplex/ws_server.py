import asyncio

import django
import websockets

from django.core.signing import TimestampSigner
from django.contrib.auth import get_user_model
from django.core.signing import SignatureExpired, BadSignature

django.setup()

User = get_user_model()

def get_user(token):
    try:
        signer = TimestampSigner()
        username = signer.unsign(token, max_age=100)
        return User.objects.get(username=username)
    except (BadSignature, SignatureExpired, User.DoesNotExist):
        return None

async def handler(websocket):
    token = await websocket.recv()
    print('Token:', token)
    user = await asyncio.to_thread(get_user, token)
    print('User:', user)
    if user is None:
        await websocket.close(1011, "authentication failed")
        return

    await websocket.send(f"Hello {user}!")


async def main():
    async with websockets.serve(handler, "localhost", 8888):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
