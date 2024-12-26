document.addEventListener("DOMContentLoaded", () => {
  const groupChatForm = document.getElementById("groupchat-form");
  const conversationForm = document.getElementById("conversation-form");
  const toggleGroupChatFormButton = document.getElementById(
    "toggle-groupchat-form"
  );
  const toggleConversationFormButton = document.getElementById(
    "toggle-conversation-form"
  );

  toggleGroupChatFormButton.addEventListener("click", () => {
    groupChatForm.classList.toggle("hidden");
    conversationForm.classList.add("hidden");
  });

  toggleConversationFormButton.addEventListener("click", () => {
    conversationForm.classList.toggle("hidden");
    groupChatForm.classList.add("hidden");
  });
});
