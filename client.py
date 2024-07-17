import asyncio
import socketio
import argparse
import sys

sio = socketio.AsyncClient()
message_history_received = asyncio.Event()


@sio.event
async def connect():
    print("Connected to server")


@sio.event
async def disconnect():
    print("Disconnected from server")


@sio.on("message_history")
async def on_message_history(data):
    print("\nMessage History:")
    for message in data:
        print(f"- {message}")
    print("\nEnter your message (or 'quit' to exit):")
    message_history_received.set()


@sio.on("update_inputs")
async def on_update_inputs(data):
    print("\nNew messages:")
    for message in data:
        print(f"- {message}")
    print("\nEnter your message (or 'quit' to exit):")


async def send_message(message):
    await sio.emit("submit_input", {"user_input": message})


async def main(server_url):
    await sio.connect(server_url)

    print("Connected to chat server. Fetching message history...")

    # Wait for message history to be received
    try:
        await asyncio.wait_for(message_history_received.wait(), timeout=5.0)
    except asyncio.TimeoutError:
        print(
            "Timed out waiting for message history. The server might not support this feature."
        )

    while True:
        message = await asyncio.get_event_loop().run_in_executor(None, input, "")
        if message.lower() == "quit":
            break
        await send_message(message)

    await sio.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command-line chat client")
    parser.add_argument(
        "server_url", help="URL of the chat server (e.g., http://192.168.1.100:5001)"
    )
    args = parser.parse_args()

    try:
        asyncio.run(main(args.server_url))
    except KeyboardInterrupt:
        print("\nExiting chat client...")
        sys.exit(0)
