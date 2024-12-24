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
1. **Docker and Docker Compose**: Ensure both are installed and running on your system.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/username/project-name.git
   cd project-name


2. Start the services using Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Verify that the services are running:

- **Flask service**: Accessible at [http://localhost:5000](http://localhost:5000).
- **FastAPI service**: Accessible at [http://localhost:8000](http://localhost:8000).
