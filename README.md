# 📚 Book Management REST API

A production-ready **Book Management REST API** built with **Django REST Framework (DRF)**. It provides secure JWT authentication, book management, filtering, searching, ordering, pagination, request throttling, and comprehensive API endpoints.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Technologies](#-key-technologies)
- [Request Flow](#-request-flow)
- [Project Structure](#-project-structure)
- [Features](#-features)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
- [Query Parameters](#-query-parameters)
- [Testing](#-testing)
- [Error Handling](#-error-handling)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📖 Overview

The **Book Management REST API** is a Django-based backend application designed to manage book information through RESTful API endpoints.

The API follows REST principles and includes authentication, authorization, filtering, searching, ordering, pagination, and request throttling.

### Key Technologies

| Technology | Version / Purpose |
|---|---|
| **Python** | 3.10+ |
| **Django** | 4.2.7 |
| **Django REST Framework** | 3.14.0 |
| **Simple JWT** | JWT authentication |
| **Django Filter** | Filtering and advanced queries |
| **SQLite3** | Development database |
| **PostgreSQL** | Recommended production database |

---

## 🔄 Request Flow

The following flow shows how a typical API request is processed:

```text
Client Request
     │
     │  GET /api/books/?search=Python
     ▼
book_management/urls.py
     │
     │ Routes request to the books application
     ▼
books/urls.py
     │
     │ DefaultRouter maps the request
     ▼
books/views.py
     │
     │ BookViewSet processes the request
     ├── Queryset: Book.objects.all()
     ├── Filtering: category, author
     ├── Searching: title, author
     ├── Ordering: title, price, published_date
     ├── Pagination: 5 books per page
     └── Permission check
     ▼
books/serializers.py
     │
     │ Converts Book objects to JSON
     ▼
JSON Response
     │
     ▼
Client
```

### For POST, PUT, PATCH, and DELETE Requests

1. The API checks whether the user is authenticated.
2. The serializer validates the submitted data.
3. Valid data is converted into a Book object.
4. The object is saved or updated in the database.
5. The API returns an appropriate response.

---

## 📁 Project Structure

```text
book_management/
│
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── book_management/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── books/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── permissions.py
    ├── filters.py
    ├── tests.py
    └── migrations/
        └── __init__.py
```

### File Responsibilities

| File | Responsibility |
|---|---|
| `models.py` | Defines the Book database model |
| `serializers.py` | Converts objects to/from JSON and validates data |
| `views.py` | Handles API request and business logic |
| `permissions.py` | Defines access-control rules |
| `filters.py` | Provides custom filtering functionality |
| `urls.py` | Defines API routes |
| `settings.py` | Contains project configuration |

---

## ✨ Features

### 📚 Book Management

- Create books
- View all books
- View individual books
- Update books
- Delete books
- Validate book information

### 🔐 Authentication & Authorization

- JWT-based authentication
- Access and refresh tokens
- Protected write operations
- Public read operations
- Permission-based access control

### 🔎 Query Features

- Filter books by category
- Filter books by author
- Search by title or author
- Sort results by title, price, or publication date
- Paginate results
- Request throttling

### ⚡ API Limits

| User Type | Request Limit |
|---|---:|
| Anonymous users | 100 requests/day |
| Authenticated users | 1,000 requests/day |

The default pagination size is **5 books per page**, with a maximum page size of **100**.

---

## 🚀 Installation

### Prerequisites

Make sure the following are installed:

- Python 3.10 or higher
- pip
- Git
- Virtual environment support

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/book-management-api.git
cd book-management-api
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

For Windows, you can also create `.env` manually from `.env.example`.

### 6. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create the administrator account.

### 8. Start the Development Server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

---

## ⚙️ Configuration

The application uses environment variables for important settings.

Example `.env` configuration:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1

# Throttling
ANON_THROTTLE_RATE=100/day
USER_THROTTLE_RATE=1000/day

# Pagination
PAGE_SIZE=5
```

### JWT Configuration

- Access tokens expire after **60 minutes**.
- Refresh tokens expire after **1 day**.
- Tokens are sent through the `Authorization` header.
- Authentication format:

```text
Authorization: Bearer <access_token>
```

### Pagination

The default page size is **5 items**.

Example:

```text
/api/books/?page=2
```

A custom page size can be requested using:

```text
/api/books/?page_size=10
```

The maximum page size is **100**.

---

# 📡 API Documentation

## 🔐 Authentication Endpoints

### 1. Obtain Access Token

```http
POST /api/token/
```

#### Request

```json
{
    "username": "admin",
    "password": "your-password"
}
```

#### Response

```json
{
    "access": "your-access-token",
    "refresh": "your-refresh-token"
}
```

---

### 2. Refresh Access Token

```http
POST /api/token/refresh/
```

#### Request

```json
{
    "refresh": "your-refresh-token"
}
```

#### Response

```json
{
    "access": "new-access-token"
}
```

---

# 📚 Book Endpoints

## 1. List All Books

**Public endpoint**

```http
GET /api/books/
```

### Examples

```http
GET /api/books/
GET /api/books/?page=2
GET /api/books/?category=Programming
GET /api/books/?search=Python
GET /api/books/?ordering=-price
```

### Example Response

```json
{
    "count": 7,
    "next": "http://localhost:8000/api/books/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Python Programming",
            "author": "John Doe",
            "category": "Programming",
            "price": "49.99",
            "published_date": "2023-01-15"
        }
    ]
}
```

---

## 2. Get a Single Book

**Public endpoint**

```http
GET /api/books/{id}/
```

Example:

```http
GET /api/books/1/
```

---

## 3. Create a Book

**Authentication required**

```http
POST /api/books/
Authorization: Bearer <access_token>
```

### Request

```json
{
    "title": "Django for Professionals",
    "author": "William S. Vincent",
    "category": "Web Development",
    "price": 39.99,
    "published_date": "2023-12-01"
}
```

---

## 4. Update a Book

**Authentication required**

### Full Update

```http
PUT /api/books/{id}/
Authorization: Bearer <access_token>
```

### Partial Update

```http
PATCH /api/books/{id}/
Authorization: Bearer <access_token>
```

---

## 5. Delete a Book

**Authentication required**

```http
DELETE /api/books/{id}/
Authorization: Bearer <access_token>
```

---

# 🔎 Query Parameters

| Parameter | Description | Example |
|---|---|---|
| `category` | Filter by category | `?category=Programming` |
| `author` | Filter by author | `?author=John%20Doe` |
| `search` | Search title and author | `?search=Python` |
| `ordering` | Sort results | `?ordering=-price` |
| `page` | Select page number | `?page=2` |
| `page_size` | Set number of results | `?page_size=10` |

### Combined Query

Multiple parameters can be used in a single request:

```http
GET /api/books/?search=Python&ordering=-price&page=2
```

This request:

- Searches for books containing **Python**
- Sorts results by price in descending order
- Returns the second page
- Applies pagination and throttling rules

---

# 🧪 Testing

## Using cURL

### 1. Get Authentication Token

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your-password"}'
```

### 2. List Books

```bash
curl http://localhost:8000/api/books/
```

### 3. Create a Book

```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Crash Course",
    "author": "Eric Matthes",
    "category": "Programming",
    "price": 29.99,
    "published_date": "2019-05-03"
  }'
```

### 4. Filter Books

```bash
curl "http://localhost:8000/api/books/?category=Programming"
```

### 5. Search Books

```bash
curl "http://localhost:8000/api/books/?search=Python"
```

### 6. Order by Price

```bash
curl "http://localhost:8000/api/books/?ordering=-price"
```

### 7. Update a Book

```bash
curl -X PUT http://localhost:8000/api/books/1/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "author": "Updated Author",
    "category": "Updated Category",
    "price": 59.99,
    "published_date": "2024-01-01"
  }'
```

### 8. Delete a Book

```bash
curl -X DELETE http://localhost:8000/api/books/1/ \
  -H "Authorization: Bearer <access_token>"
```

---

## 📮 Testing with Postman

You can also test the API using **Postman**.

1. Set the base URL:

```text
http://localhost:8000
```

2. Obtain an access token from:

```text
POST /api/token/
```

3. Add the token to protected requests:

```text
Authorization: Bearer <access_token>
```

4. Test GET, POST, PUT, PATCH, and DELETE endpoints.

---

# ❌ Error Handling

The API uses standard HTTP status codes.

| Status | Meaning | Typical Cause |
|---|---|---|
| **400** | Bad Request | Invalid data |
| **401** | Unauthorized | Missing or invalid authentication |
| **403** | Forbidden | Insufficient permission |
| **404** | Not Found | Resource does not exist |
| **429** | Too Many Requests | Rate limit exceeded |

### Example

```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

# 🐛 Debugging

### Database Problems

If you need to reset the development database:

```bash
python manage.py flush
python manage.py makemigrations
python manage.py migrate
```

### JWT Problems

Check the following:

- The token is valid.
- The token has not expired.
- The request contains the correct header.
- The authentication format is:

```text
Authorization: Bearer <access_token>
```

If the access token has expired, use the refresh endpoint.

### Permission Problems

Make sure:

- The user is authenticated.
- The correct access token is being used.
- The user has the required permissions.

---

# 🚀 Deployment

Before deploying to production, complete the following checklist:

- [ ] Generate a strong `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure production `ALLOWED_HOSTS`
- [ ] Use PostgreSQL or another production-ready database
- [ ] Configure HTTPS/SSL
- [ ] Store secrets in environment variables
- [ ] Configure CORS properly
- [ ] Enable logging and monitoring
- [ ] Configure database backups
- [ ] Run Django security checks

Run:

```bash
python manage.py check --deploy
```

---

## Gunicorn Deployment

Install production dependencies:

```bash
pip install gunicorn psycopg2-binary
```

Collect static files:

```bash
python manage.py collectstatic --noinput
```

Apply migrations:

```bash
python manage.py migrate
```

Start Gunicorn:

```bash
gunicorn --workers 4 \
         --bind 0.0.0.0:8000 \
         book_management.wsgi
```

A reverse proxy such as **Nginx** can be placed in front of Gunicorn to handle incoming HTTP/HTTPS traffic.

---

## 🐳 Docker Deployment

Example `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "book_management.wsgi"]
```

Example `docker-compose.yml`:

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      DEBUG: "False"
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: books
      POSTGRES_USER: books_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

# 🤝 Contributing

Contributions are welcome.

### Steps

1. Fork the repository.
2. Create a feature branch:

```bash
git checkout -b feature/amazing-feature
```

3. Commit your changes:

```bash
git commit -m "Add amazing feature"
```

4. Push the branch:

```bash
git push origin feature/amazing-feature
```

5. Open a Pull Request.

---

# 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for more information.

---

# 📞 Support

If you encounter an issue, please create an issue in the GitHub repository with:

- A clear description of the problem
- Steps to reproduce it
- Relevant error messages
- Environment details

---

<div align="center">

### ❤️ Built with Django REST Framework

**Book Management REST API**

</div>
