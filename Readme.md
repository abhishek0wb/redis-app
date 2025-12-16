# AI Microservice Queueing System

A scalable microservice-based system for handling **computationally expensive AI tasks asynchronously** without blocking user-facing APIs.

This project separates request handling from AI processing using Redis, allowing the API to respond instantly while heavy computation runs in the background.

---

## Problem

AI tasks such as summarization are slow and resource-intensive.  
Processing them synchronously leads to:

- Slow API responses
- Request timeouts
- Poor scalability

---

## Solution

This system uses:

- Asynchronous job processing
- Redis as a message queue and pub/sub broker
- Independent microservices for API and AI computation

The API immediately queues the task and returns a response, while processing happens separately.

---

## Architecture

The system consists of three services:

### API Gateway (NestJS – TypeScript)
- Accepts client requests
- Validates input
- Pushes jobs to Redis
- Listens for completion events

### Redis (Message Broker)
- Stores jobs in a queue
- Publishes job completion events

### AI Worker (Python)
- Pulls jobs from Redis
- Processes AI tasks using Google Gemini API
- Publishes results back to Redis

All services are containerized and managed using Docker Compose.

---

## Execution Flow

1. Client sends a POST request to the API  
2. API queues the job and responds with `status: queued`  
3. Worker processes the job in the background  
4. Result is published and consumed via Redis Pub/Sub  

---

## Tech Stack

- NestJS (TypeScript)
- Python
- Redis
- Docker & Docker Compose
- Google Gemini API

---

## Setup

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
REDIS_HOST=redis
```


---


## Build and run the services

```
docker-compose up --build
```

---


## Test Request

```
curl -X POST http://localhost:3000/process \
-H "Content-Type: application/json" \
-d '{"text":"This is a long article about software engineering and microservices."}'
```