import requests

BASE_URL = "http://backend:8000"


def get_conversations():
    """Fetch all conversations."""
    response = requests.get(f"{BASE_URL}/conversations")
    response.raise_for_status()
    return response.json()


def get_conversations_by_user(user_id):
    """Fetch all conversations for a specific user."""
    response = requests.get(f"{BASE_URL}/conversations/{user_id}")
    response.raise_for_status()
    return response.json()


def get_groupchats():
    """Fetch all groupchats."""
    response = requests.get(f"{BASE_URL}/groupchats")
    response.raise_for_status()
    return response.json()


def get_groupchats_by_user(user_id):
    """Fetch all group chats for a specific user."""
    response = requests.get(f"{BASE_URL}/groupchats/{user_id}")
    response.raise_for_status()
    return response.json()


def create_conversation(user1_id, user2_id, name):
    """Create a new conversation."""
    payload = {"user1_id": user1_id, "user2_id": user2_id, "name": name}
    response = requests.post(f"{BASE_URL}/conversations", json=payload)
    response.raise_for_status()
    return response.json()


def create_group_chat(admin_id, name):
    """Create a new group chat."""
    payload = {"admin_id": admin_id, "name": name}
    response = requests.post(f"{BASE_URL}/groupchats", json=payload)
    response.raise_for_status()
    return response.json()


def add_member_to_group(group_id, user_id):
    """Add a member to a group chat."""
    payload = {"user_id": user_id}
    response = requests.post(
        f"{BASE_URL}/groupchats/{group_id}/add_member", json=payload
    )
    response.raise_for_status()


def signup(username, email):
    """Sign up a new user."""
    payload = {"username": username, "email": email}
    response = requests.post(f"{BASE_URL}/signup", json=payload)
    response.raise_for_status()
    return response.json()


def signin(username):
    """Sign in an existing user."""
    payload = {"username": username}
    response = requests.post(f"{BASE_URL}/signin", json=payload)
    response.raise_for_status()
    return response.json()


def get_conversation_messages(conversation_id):
    """Fetch messages for a specific conversation."""
    response = requests.get(f"{BASE_URL}/messages/conversation/{conversation_id}")
    response.raise_for_status()
    return response.json()


def get_groupchat_messages(groupchat_id):
    """Fetch messages for a specific conversation."""
    response = requests.get(f"{BASE_URL}/messages/groupchat/{groupchat_id}")
    response.raise_for_status()
    return response.json()


def send_conversation_message(conversation_id, sender_id, content):
    """Send a message to a specific conversation."""
    payload = {
        "sender_id": sender_id,
        "conversation_id": conversation_id,
        "content": content,
        "groupchat_id": 0,
    }
    response = requests.post(f"{BASE_URL}/messages/conversation", json=payload)
    response.raise_for_status()
    return response.json()


def send_groupchat_message(groupchat_id, sender_id, content):
    """Send a message to a specific conversation."""
    payload = {
        "sender_id": sender_id,
        "groupchat_id": groupchat_id,
        "content": content,
        "conversation_id": 0,
    }
    response = requests.post(f"{BASE_URL}/messages/groupchat", json=payload)
    response.raise_for_status()
    return response.json()


def get_user_by_username(username):
    """Fetch a specific user by their username."""
    response = requests.get(f"{BASE_URL}/users/username/{username}")
    response.raise_for_status()
    return response.json()

def get_user_by_id(user_id):
    """Fetch a specific user by their id."""
    response = requests.get(f"{BASE_URL}/users/id/{user_id}")
    response.raise_for_status()
    return response.json()

def delete_conversation(conversation_id):
    """Delete a specific conversation."""
    response = requests.delete(f"{BASE_URL}/conversations/{conversation_id}")
    response.raise_for_status()
    return response.json()


def delete_groupchat(groupchat_id, user_id):
    """Delete a specific group chat."""
    response = requests.delete(
        f"{BASE_URL}/groupchats/{groupchat_id}?user_id={user_id}"
    )
    response.raise_for_status()
    return response.json()