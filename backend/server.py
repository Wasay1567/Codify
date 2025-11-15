from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn
from utitls import generate_random_id
import json

app = FastAPI()

users = {}

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>

        <label for="username">Name:</label>
        <input type="text" id="username" autocomplete="off" placeholder="Enter your name"/>
        <button id="connectBtn" onclick="connect()">Connect</button>

        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>

        <ul id='messages'></ul>

        <script>
            var ws = null;

            function connect() {
                if (ws) return;
                var name = document.getElementById("username").value || "anonymous";
                ws = new WebSocket("ws://localhost:8080/ws");

                ws.onopen = function() {
                    // send user name after connecting
                    ws.send(JSON.stringify({ name: name }));
                };

                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages');
                    var message = document.createElement('li');
                    var content = document.createTextNode(event.data);
                    message.appendChild(content);
                    messages.appendChild(message);
                };

                ws.onclose = function() { ws = null; };
            }

            function sendMessage(event) {
                event.preventDefault();
                var input = document.getElementById("messageText");
                if (!ws) {
                    alert("Please connect first");
                    return;
                }
                ws.send(input.value);
                input.value = '';
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # first message must contain user JSON
    first_msg = await websocket.receive_text()
    user_data = json.loads(first_msg)
    username = user_data.get("name", "anonymous")

    user_id = generate_random_id()
    users[user_id] = websocket

    await websocket.send_text(f"User {username} connected with ID {user_id}")

    # now normal chat messages
    while True:
        msg = await websocket.receive_text()
        await broadcast(f"{username}: {msg}")

async def broadcast(message: str):
    for user_ws in users.values():
        await user_ws.send_text(message)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
