import websocket
import time


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    async def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
            print(ws.recv())
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    res = run()


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "ws://127.0.0.1:8000/feed",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
