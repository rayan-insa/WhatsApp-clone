from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils.api import *
import requests

app = Flask(__name__)
app.secret_key = "very_secret"


@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("signin_route"))
    user_id = session["user_id"]
    conversations = get_conversations_by_user(user_id)
    for conversation in conversations:
        receiver_id = (
            conversation["user1_id"]
            if conversation["user2_id"] == user_id
            else conversation["user2_id"]
        )
        receiver_username = get_user_by_id(receiver_id)["username"]
        conversation["name"] = (
            conversation["name"] if conversation["name"] else receiver_username
        )
    groupchats = get_groupchats_by_user(session["user_id"])
    return render_template(
        "home.html",
        conversations=conversations,
        groupchats=groupchats,
        current_user=session["username"],
    )


@app.route("/messages/conversation/<int:conversation_id>")
def chat_conversation(conversation_id):
    if "user_id" not in session:
        return redirect(url_for("signin_route"))
    messages = get_conversation_messages(conversation_id)
    conversations = get_conversations()
    conversation = next((c for c in conversations if c["id"] == conversation_id), None)
    reciever_id = (
        conversation["user1_id"]
        if conversation["user2_id"] == session["user_id"]
        else conversation["user2_id"]
    )
    reciever_username = get_user_by_id(reciever_id)["username"]
    if conversation["name"]:
        chat_name = conversation["name"]
    else:
        chat_name = reciever_username
    return render_template(
        "chat.html",
        chat_name=chat_name,
        messages=messages,
        chat_id=conversation_id,
        current_user=session.get("username"),
    )


@app.route("/messages/groupchat/<int:groupchat_id>")
def chat_groupchat(groupchat_id):
    if "user_id" not in session:
        return redirect(url_for("signin_route"))
    messages = get_groupchat_messages(groupchat_id)
    groupchats = get_groupchats()
    groupchat = next((c for c in groupchats if c["id"] == groupchat_id), None)
    if groupchat:
        chat_name = groupchat["name"]
    else:
        chat_name = f"groupchat {groupchat_id}"
    return render_template(
        "chat.html",
        chat_name=chat_name,
        messages=messages,
        chat_id=groupchat_id,
        current_user=session.get("username"),
        is_admin=groupchat["admin_id"] == session["user_id"],
    )


@app.route("/messages/conversation/<int:conversation_id>/send", methods=["POST"])
def send_conversation_message_route(conversation_id):
    if "user_id" not in session:
        return redirect(url_for("signin_route"))
    content = request.form["message"]
    send_conversation_message(
        conversation_id=conversation_id,
        sender_id=session["user_id"],
        content=content,
    )
    return redirect(url_for("chat_conversation", conversation_id=conversation_id))


@app.route("/messages/groupchat/<int:groupchat_id>/send", methods=["POST"])
def send_groupchat_message_route(groupchat_id):
    if "user_id" not in session:
        return redirect(url_for("signin_route"))
    content = request.form["message"]
    send_groupchat_message(
        groupchat_id=groupchat_id,
        sender_id=session["user_id"],
        content=content,
    )
    return redirect(url_for("chat_groupchat", groupchat_id=groupchat_id))


@app.route("/signup", methods=["GET", "POST"])
def signup_route():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        try:
            user = signup(username, email)
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("home"))
        except requests.exceptions.HTTPError as e:
            error_message = e.response.json().get("detail", "Signup failed")
            return render_template("signup.html", error=error_message)
    return render_template("signup.html")


@app.route("/signin", methods=["GET", "POST"])
def signin_route():
    if request.method == "POST":
        username = request.form["username"]
        try:
            user = signin(username)
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("home"))
        except requests.exceptions.HTTPError as e:
            error_message = e.response.json().get("detail", "Signin failed")
            return render_template("signin.html", error=error_message)
    return render_template("signin.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("signin_route"))


@app.route("/conversations/create", methods=["POST"])
def create_conversation_route():
    if "user_id" not in session:
        return redirect(url_for("signin_route"))
    try:
        user1_id = session["user_id"]
        username2 = request.form["username"]
        user2_id = get_user_by_username(username2)["id"]

        if user1_id == user2_id:
            error_message = "You cannot create a conversation with yourself."
            flash(error_message)
            return redirect(url_for("home"))
        name = request.form.get("name")
        conversation = create_conversation(
            user1_id=user1_id, user2_id=user2_id, name=name
        )

        return redirect(
            url_for("chat_conversation", conversation_id=conversation["id"])
        )
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json().get("detail", "Failed to create conversation")
        flash(error_message)
        return redirect(url_for("home"))
    except Exception as e:
        error_message = str(e)
        flash(error_message)
        return redirect(url_for("home"))


@app.route("/groupchats/create", methods=["POST"])
def create_groupchat_route():
    if "user_id" not in session:
        return redirect(url_for("signin_route"))

    group_name = request.form["name"]
    members = request.form["members"]

    member_usernames = [
        username.strip() for username in members.split(",") if username.strip()
    ]

    member_user_ids = []
    for username in member_usernames:
        user = get_user_by_username(username)
        if user:
            member_user_ids.append(user["id"])
        else:
            error_message = f"User {username} not found"
            flash(error_message)
            return redirect(url_for("home"))

    try:
        group_response = create_group_chat(session["user_id"], group_name)

        group_id = group_response["group_chat"]["id"]
        try:
            add_member_to_group(group_id, session["user_id"])
        except requests.exceptions.HTTPError as e:
            error_message = f"Failed to add member {username}: {e}"
            flash(error_message)
            return redirect(url_for("home"))
        for user_id in member_user_ids:
            try:
                add_member_to_group(group_id, user_id)
            except requests.exceptions.HTTPError as e:
                error_message = f"Failed to add member {user_id}: {e}"
                flash(error_message)
                return redirect(url_for("home"))

        return redirect(url_for("chat_groupchat", groupchat_id=group_id))
    except requests.exceptions.HTTPError as e:
        group_error = e.response.json().get(
            "detail", "An error occurred while creating the group chat."
        )
        flash(group_error)
        return redirect(url_for("home"))


@app.route("/groupchat/<int:groupchat_id>/add_member", methods=["POST"])
def add_member_route(groupchat_id):
    if "user_id" not in session:
        return redirect(url_for("signin_route"))

    username = request.form["username"]
    user_id = get_user_by_username(username)["id"]

    try:
        add_member_to_group(groupchat_id, user_id)
        flash(f"User '{username}' was successfully added to the group!", "success")
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json().get("detail", "An error occurred.")
        flash(f"Failed to add member: {error_message}")

    return redirect(url_for("chat_groupchat", groupchat_id=groupchat_id))


@app.route("/conversation/<int:conversation_id>/delete", methods=["POST"])
def delete_conversation_route(conversation_id):
    if "user_id" not in session:
        return redirect(url_for("signin_route"))
    try:
        delete_conversation(conversation_id)
        flash("Conversation deleted successfully.", "success")
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json().get("detail", "An error occurred.")
        flash(f"Failed to delete conversation: {error_message}", "danger")
    return redirect(url_for("home"))


@app.route("/groupchat/<int:groupchat_id>/delete", methods=["POST"])
def delete_groupchat_route(groupchat_id):
    if "user_id" not in session:
        return redirect(url_for("signin_route"))
    groupchat = next((g for g in get_groupchats() if g["id"] == groupchat_id), None)
    if not groupchat or groupchat["admin_id"] != session["user_id"]:
        flash("You are not authorized to delete this group chat.", "danger")
        return redirect(url_for("chat_groupchat", groupchat_id=groupchat_id))
    try:
        delete_groupchat(groupchat_id, session["user_id"])
        flash("Group chat deleted successfully.", "success")
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json().get("detail", "An error occurred.")
        flash(f"Failed to delete group chat: {error_message}", "danger")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
