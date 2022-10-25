import asyncio
import pty
import websockets
import os
import subprocess

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
        await consumer_q.put(message)


async def producer_handler(websocket):
    while True:
        await websocket.send(await producer_q.get())


async def handler():
    loop = asyncio.get_event_loop()
    loop.add_reader(master_fd, read_pty)
    loop.add_writer(master_fd, write_pty)
    async with websockets.connect("ws://localhost:1234") as websocket:
        print("connected")
        await asyncio.gather(
            consumer_handler(websocket),
            producer_handler(websocket),
        )


asyncio.run(handler())
