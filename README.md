# 📚 Microservices Architecture with FastAPI, Docker, and NGINX

This repository showcases a Microservices architecture built with FastAPI, Docker, and NGINX. It integrates multiple services like Auth, Order, Payment, and a Config Service, providing a dynamic and flexible microservice-based system.

This system uses tools such as Eureka for service discovery, RabbitMQ for message queuing, MySQL for database storage, and NGINX as a reverse proxy to route traffic.

---

## 🚀 Project Overview

The project demonstrates the following:

- Service Discovery with Eureka
- Rate Limiting and Caching with NGINX
- Centralized Configuration Management with Config Service
- Message Queueing with RabbitMQ
- Database interaction using MySQL with Python
- FastAPI framework for building microservices

---

## 🧑‍💻 Technologies Used

- **FastAPI**: Modern web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **Docker**: Used for containerizing all the services and ensuring easy deployment and scalability.
- **NGINX**: Acts as a reverse proxy server, handling rate limiting, caching, and routing.
- **RabbitMQ**: Message queue service for decoupling services.
- **MySQL**: Relational database for storing orders in the Payment Service.
- **Eureka**: Service registry for service discovery.
- **PyEureka Client**: Python client for integrating with Eureka.

---

## 📋 Architecture Diagram

┌───────────────────────────┐
│       NGINX Gateway        │
└─────┬──────┬──────────────┘
      │      │
┌─────┼──────┼────────┐
▼     ▼      ▼        ▼
Auth Service   Order Service   Payment Service
(Login)        (Create Order)  (Process Payment)
│              │               │
▼              ▼               ▼
Config Service   RabbitMQ       MySQL (Database)
│
┌─────┴─────┐
│   Eureka   │
└───────────┘


---

## 🛠️ Services in the Project

### 1. Auth Service

- **Purpose**: Responsible for handling login requests and generating JWT tokens.
- **Endpoints**:
  - `/login`: Accepts username and password, generates JWT token if valid.
  - `/validate`: Validates the JWT token.

### 2. Order Service

- **Purpose**: Handles creating orders, sends order data to RabbitMQ for processing.
- **Endpoints**:
  - `/create-order`: Creates a new order and sends it to RabbitMQ.
  - Retrieves configuration from Config Service for RabbitMQ URL and payment service name.

### 3. Payment Service

- **Purpose**: Processes payments for the orders. Listens for messages in RabbitMQ and updates the database.
- **Endpoints**:
  - `/process-payment`: Receives orders and processes payments.
  - `/orders`: Returns all stored orders from the database.

### 4. Config Service (NEW)

- **Purpose**: Centralized configuration management for all microservices.
- **Endpoints**:
  - `/config/{service_name}`: Retrieves configuration for a specified service.
  - Serves configurations like `SECRET_KEY`, `MYSQL_CONFIG`, `RABBITMQ_URL`, etc.

---

## 🧑‍💻 How the System Works

1. **NGINX** serves as a reverse proxy. It routes requests to various services like Auth, Order, and Payment.
   - It applies rate limiting for the `/order` endpoint and caching for `/orders`.

2. **Eureka** handles service discovery. Each service registers itself with Eureka and can discover other services based on their name.

3. **Auth Service** is responsible for generating JWT tokens for users. After successful login, users can make requests to Order Service and Payment Service by passing the token in the authorization header.

4. **Order Service** creates orders and sends the order data to RabbitMQ. It also calls the Payment Service to process the payment.

5. **Payment Service** listens to RabbitMQ and processes orders. It interacts with the MySQL database to store orders.

6. **Config Service** manages configurations like secrets, database credentials, and service URLs. It dynamically serves the configuration for each microservice via API requests.

---

## 🛠️ Running the Project

### Prerequisites:

- Docker and Docker Compose installed.

### Steps to Run:

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/microservices-example.git
    cd microservices-example
    ```

2. Build and start all services with Docker Compose:

    ```bash
    docker-compose up --build
    ```

3. Access the services:

- **Auth Service**: http://localhost:8002
- **Order Service**: http://localhost:8000
- **Payment Service**: http://localhost:8001
- **NGINX Gateway**: http://localhost:8080
- **Config Service**: http://localhost:8003

---

## 🧑‍🏫 Learning Objectives and How to Learn from This Repo

1. **Microservices Communication**:
   - Learn how different microservices communicate with each other using REST APIs and message queues (RabbitMQ).

2. **Service Discovery**:
   - Understand how Eureka enables microservices to register themselves and discover each other dynamically.

3. **API Gateway with NGINX**:
   - Learn how NGINX can be used as a reverse proxy to route requests, implement caching, and apply rate limiting for security and performance.

4. **Centralized Configuration**:
   - Learn how to build and use a Config Service to manage application configurations centrally and dynamically.

5. **Error Handling**:
   - Discover how to handle errors and failures in microservices using circuit breakers and retries (RabbitMQ).

---

## 🏁 Project Structure

.
├── auth_service/
│   ├── app.py             # Auth service code
│   ├── Dockerfile         # Docker configuration
│   ├── requirements.txt   # Required libraries
│
├── nginx/
│   ├── nginx.conf         # NGINX configuration
│
├── order_service/
│   ├── app.py             # Order service code
│   ├── Dockerfile         # Docker configuration
│   ├── requirements.txt   # Required libraries
│
├── payment_service/
│   ├── app.py             # Payment service code
│   ├── Dockerfile         # Docker configuration
│   ├── requirements.txt   # Required libraries
│   ├── db.py              # MySQL database code
│   ├── consumer.py        # RabbitMQ consumer
│
├── config_service/
│   ├── app.py             # Config service code
│   ├── config.json        # Configuration JSON
│   ├── Dockerfile         # Docker configuration
│   ├── requirements.txt   # Required libraries
│
└── docker-compose.yml     # Docker Compose configuration



---

## 🔐 Security Considerations

- **JWT Authentication**: Auth services generate JWT tokens for user authentication.
- **Environment Variables**: Sensitive data such as database credentials and secrets are stored securely and managed via the Config Service.

---

## 🚨 Further Improvements

1. **Add Monitoring and Metrics**:
   - Integrate Prometheus and Grafana to monitor the health and performance of the services.

2. **Database Scaling**:
   - Consider horizontal scaling of the database and add read replicas for high availability.

3. **Advanced Error Handling**:
   - Implement more sophisticated error handling with retries, dead-letter queues (DLQ), and better circuit breaker patterns.

4. **CI/CD Integration**:
   - Set up a CI/CD pipeline with tools like GitHub Actions, GitLab CI, or Jenkins.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 💬 Contact

Feel free to reach out to me for any questions or suggestions!

---

🎉 Enjoy Learning Microservices! 🎉


