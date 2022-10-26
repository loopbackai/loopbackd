import asyncio
import pty
import websockets
import os
import subprocess
import json
import base64
import sys

master_fd, slave_fd = pty.openpty()
producer_q = asyncio.Queue()
consumer_q = asyncio.Queue()

p = subprocess.Popen(
    ["bash"],
    stdin=slave_fd,
    stdout=slave_fd,
    stderr=slave_fd,
    # Run in a new process group to enable bash's job control.
    preexec_fn=os.setsid,
    # Run bash in "dumb" terminal.
    env=dict(os.environ, TERM="dumb"),
)


def read_pty():
    output = os.read(master_fd, 10240)
    # os.write(sys.stdout.fileno(), output)
    producer_q.put_nowait(output)


def write_pty():
    while not consumer_q.empty():
        user_input: str = consumer_q.get_nowait()
        os.write(master_fd, user_input.encode("utf-8"))


async def consumer_handler(websocket):
    async for message in websocket:
        print("RECEIVED:", message)
        message = json.loads(message)
        if message["event"] == "new_command":
            await consumer_q.put(message["payload"])
        # await consumer_q.put(message)


async def producer_handler(websocket):
    while True:
        message = await producer_q.get()
        print("SENDING: ", message)
        await websocket.send(
            json.dumps(
                {
                    "topic": "loopback:chen123",
                    "event": "data",
                    "payload": base64.b64encode(message).decode("utf-8"),
                    "ref": "",
                    "join_ref": "",
                }
            )
        )
        # await websocket.send(await producer_q.get())


async def handler():
    loop = asyncio.get_event_loop()
    loop.add_reader(master_fd, read_pty)
    loop.add_writer(master_fd, write_pty)

    # poll process and terminate when process exit
    def poll_process():
        if p.poll() is not None:
            loop.stop()
            sys.exit(0)
        loop.call_soon(poll_process)

    loop.call_soon(poll_process)

    async with websockets.connect(
        "wss://3de4-77-137-70-101.ngrok.io/socket/websocket"
    ) as websocket:
        await websocket.send(
            json.dumps(
                {
                    "topic": "loopback:chen123",
                    "event": "phx_join",
                    "payload": "",
                    "ref": "",
                    "join_ref": "",
                }
            )
        )
        await asyncio.gather(
            consumer_handler(websocket),
            producer_handler(websocket),
        )


asyncio.run(handler())
