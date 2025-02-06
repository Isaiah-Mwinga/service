# 🚀 FastAPI Microservices - Customer Order API

This project is a microservices-based API built with **FastAPI**, **PostgreSQL**, **Celery**, and **Auth0 OpenID Connect** for authentication. It handles customer orders, authentication, and asynchronous background tasks.

---

## 📌 Features
✅ OpenID Connect Authentication (Auth0)  
✅ CRUD operations for Customers & Orders  
✅ Asynchronous background tasks (SMS notifications using Celery)  
✅ PostgreSQL Database with SQLAlchemy & Alembic Migrations  
✅ Dockerized for deployment  
✅ CI/CD with GitHub Actions  

---

## 🛠️ **Tech Stack**
- **Backend:** FastAPI, Pydantic, SQLAlchemy  
- **Database:** PostgreSQL  
- **Task Queue:** Celery + Redis  
- **Authentication:** OpenID Connect (Auth0)  
- **Containerization:** Docker, Docker Compose  
- **CI/CD:** GitHub Actions  

---

## 🚀 **Getting Started**

### 🔹 **1. Clone the repository**
```sh
git clone https://github.com/Isaiah-Mwinga/service.git
cd your-repo
create a virtual envronment
Install your dependecies in requirements.txt
Run the code from run.sh

Start redis container if youre using docker
start celery and make sure its connected to redis
```

### 🔹 **2. Add an image**

![Sucess Message on Africastalking]
![alt text](<Screenshot 2025-02-05 214723.png>)