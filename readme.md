# 📱 Social Media API (FastAPI)

A simple yet powerful **Social Media Backend API** built using **FastAPI** and **SQLAlchemy**.  
This API supports **User Authentication, Posts, Likes, and Comments** functionality.

---

## 🚀 Features

- **User Authentication**  
  - Sign Up (Register new users)  
  - Login with JWT Token Authentication  
  - Secure password hashing  

- **Posts Management**  
  - Create, Read, Update, Delete posts  
  - View all posts or a single post  

- **Likes System**  
  - Like or Unlike a post  

- **Comments System**  
  - Add comments to a post  
  - View all comments on a post  
  - Update and delete own comments  

---

## 🛠️ Tech Stack

- **Backend Framework** → FastAPI
- **ORM** → SQLAlchemy
- **Database** → SQLite (can be switched to PostgreSQL/MySQL)
- **Authentication** → JWT (JSON Web Token)
- **Password Security** → Passlib (bcrypt hashing)
- **API Docs** → Swagger UI & ReDoc

---

## 📂 Project Structure

src/
├── main.py        # Application entry point
├── database.py    # Database connection setup
├── models.py      # SQLAlchemy models
├── schemas.py     # Pydantic schemas
├── auth.py        # Authentication & JWT logic
├── crud.py        # CRUD functions
└── routers/
├── users.py   # User routes
├── posts.py   # Post routes
├── likes.py   # Like routes
└── comments.py # Comment routes

---

## ⚡ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/abhishekKumar253/backend-intern-crud.git
cd backend-intern-crud
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the application

```bash
uvicorn src.main:app --reload
```

🔑 Authentication Flow (JWT)

1. Register → /api/users/register
2.Login → /api/users/login → Get access_token from response
3.Use Token → Add Authorization: Bearer <your_token> in headers for protected routes.

📌 API Documentation

Once server is running, visit:

Swagger UI → <http://127.0.0.1:8000/docs>

ReDoc → <http://127.0.0.1:8000/redoc>

🧪 Example API Endpoints
Method Endpoint Description
POST /api/users/register Register new user
POST /api/users/login Login and get JWT token
GET /api/posts Get all posts
POST /api/posts Create new post
PUT /api/posts/{post_id} Update a post
DELETE /api/posts/{post_id} Delete a post
POST /api/posts/{post_id}/like Like/Unlike a post
POST /api/posts/{post_id}/comments Add comment to a post
PUT /api/posts/comments/{id} Update own comment
DELETE /api/posts/comments/{id} Delete own comment

📝 API Docs
Swagger UI → <http://127.0.0.1:8000/docs>

ReDoc → <http://127.0.0.1:8000/redoc>

👨‍💻 Author
Abhishek
