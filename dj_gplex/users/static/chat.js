/*jshint esversion: 6 */

function sendMessages(websocket) {
  const sendbtn = document.getElementById("sendbtn");
  const sendmsg = document.getElementById("sendmsg");

  sendbtn.addEventListener("click", event => {
    const message = {
      type: "chat",
      from: USERNAME,
      to: USERNAME,
      message: sendmsg.value
    };
    websocket.send(JSON.stringify(message));
    console.log("WS> " + JSON.stringify(message));
    sendmsg.value = "";
    event.preventDefault();
  });
}


function receiveMessages(websocket) {
  websocket.addEventListener("message", ({ data }) => {
    console.log("WS< " + data);
    const event = JSON.parse(data);
    switch (event.type) {
      case "chat":
        //TODO: add the message to the chat ui
        showMessage(event.message);
        break;
      default:
        throw new Error(`Unsupported event type: ${event.type}.`);
    }
  });
}


function showMessage(message) {
  window.setTimeout(() => window.alert(message), 50);
}

function initSocket(websocket) {
  websocket.addEventListener("open", () => {
    websocket.send(WS_AUTH_TOKEN);
  });
}

window.addEventListener("DOMContentLoaded", () => {
  const websocket = new WebSocket("ws://localhost:8888/");
  initSocket(websocket);
  receiveMessages(websocket);
  sendMessages(websocket);
});
