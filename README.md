# Messaging Web App with Kafka Integration

This is a distributed messaging web application built using Flask, FastAPI, MySQL, and Kafka. The application allows users to sign in, sign up, create group chats, send and receive messages, and perform other actions concurrently with multiple users, leveraging Kafka for multithreading and event-driven communication.

---

## Features

- **User Authentication**: Users can sign in and sign up.
- **Messaging**: Send and receive messages in private conversations and group chats.
- **Group Chat Management**: Create, delete (admin-only), and manage members in group chats.
- **Kafka Integration**: Use Kafka for multithreading and enabling real-time concurrent actions across multiple users.
- **Scalable Architecture**: Designed for distributed systems using Docker, Flask, FastAPI, and MySQL.

---

## Tech Stack

### Backend:
- **Flask**: Frontend API.
- **FastAPI**: Backend API for handling core business logic.
- **MySQL**: Database for storing user data, messages, and group chat information.
- **Kafka**: Event streaming for multithreaded communication.
- **Confluent Kafka Client**: Python library for interacting with Kafka.

### Frontend:
- **HTML, CSS, JavaScript**: For building the user interface.
- **Bootstrap**: For responsive and clean design.

### Deployment:
- **Docker**: Containerization of services for scalability.

---

## Installation

### Prerequisites
1. **Python 3.10+**
2. **Docker and Docker Compose**
3. **Kafka**: Install Kafka and Zookeeper binaries ([instructions](https://kafka.apache.org/quickstart)).

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/username/project-name.git
   cd project-name
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start Kafka and Zookeeper:
   ```bash
   # Navigate to Kafka directory
   bin/zookeeper-server-start.sh config/zookeeper.properties
   bin/kafka-server-start.sh config/server.properties
   ```

5. Start the MySQL server and set up the database:
   ```sql
   CREATE DATABASE messaging_app;
   ```

6. Apply database migrations (if applicable).

7. Start the Flask server:
   ```bash
   flask run
   ```

8. Start the FastAPI server:
   ```bash
   uvicorn backend.main:app --reload
   ```

9. Start the Kafka consumer:
   ```bash
   python consumer.py
   ```
