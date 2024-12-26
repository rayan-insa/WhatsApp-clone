document.addEventListener("DOMContentLoaded", () => {
  const groupChatForm = document.getElementById("groupchat-form");
  const conversationForm = document.getElementById("conversation-form");
  const toggleGroupChatFormButton = document.getElementById(
    "toggle-groupchat-form"
  );
  const toggleConversationFormButton = document.getElementById(
    "toggle-conversation-form"
  );

  // toggleGroupChatFormButton.addEventListener("click", () => {
  //   groupChatForm.classList.toggle("hidden");
  //   conversationForm.classList.add("hidden");
  // });

  // toggleConversationFormButton.addEventListener("click", () => {
  //   conversationForm.classList.toggle("hidden");
  //   groupChatForm.classList.add("hidden");
  // });

  // WebSocket connection
  console.log("Connecting to WebSocket server...");
  const ws = new WebSocket(`ws://localhost:8000/ws`);
  console.log(`Connected to WebSocket server at ws://backend:8000/ws`);

  ws.onopen = function (event) {
    console.log("WebSocket is open now.");
  };

  ws.onmessage = function (event) {
    console.log("Received message: " + event.data);
    const message = event.data;
    if (message === "New message") {
      location.reload();
    }
  };

  ws.onclose = function (event) {
    console.log("WebSocket is closed now.");
  };

  ws.onerror = function (event) {
    console.error("WebSocket error observed:", event);
  };
});
