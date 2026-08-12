# Book Management REST API

> A production-ready Book Management REST API built with Django REST Framework featuring JWT authentication, filtering, searching, ordering, pagination, and rate limiting.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Request Flow](#request-flow)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This is a production-grade REST API for managing books with complete authentication and authorization controls. The API implements industry best practices including JWT-based authentication, request throttling, comprehensive filtering, and pagination.

**Key Technologies:**
- Django 4.2.7
- Django REST Framework 3.14.0
- JWT Authentication (Simple JWT)
- Django Filter
- SQLite3 (Development) / PostgreSQL (Production)

---

## Request Flow

Understanding the request lifecycle helps debug issues and understand how the application works:

```
Client Request (GET /books/?search=Python)
    │
    ▼
book_management/urls.py
    │  └── Routes request to appropriate app
    ▼
books/urls.py
    │  └── DefaultRouter maps /books/ to BookViewSet
    ▼
books/views.py
    │  └── BookViewSet.list() executes
    │      ├── 1. Queryset: Book.objects.all()
    │      ├── 2. Filter Backends:
    │      │   ├── DjangoFilterBackend (category, author)
    │      │   ├── SearchFilter (title, author)
    │      │   └── OrderingFilter (title, price, published_date)
    │      ├── 3. Pagination: 5 results per page
    │      └── 4. Permission Check: AllowAny (GET requests are public)
    ▼
books/serializers.py
    │  └── BookSerializer converts Book objects to JSON
    ▼
JSON Response (Returns to Client)
```

**For POST/PUT/DELETE Requests:**
- Permission check occurs before processing: `IsAuthenticated` required
- Serializer validates incoming JSON data
- Data is converted to Book object (deserialization)
- Valid data is saved to database
- Response returns the created/updated object

---

## Project Structure

```
book_management/
├── manage.py                      # Django's command-line utility
├── requirements.txt               # Project dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore file
├── README.md                      # This file
│
├── book_management/               # Project configuration
│   ├── __init__.py
│   ├── settings.py                # All project settings
│   ├── urls.py                    # Main URL configuration
│   ├── asgi.py                    # ASGI configuration
│   └── wsgi.py                    # WSGI configuration
│
└── books/                         # Main application
    ├── __init__.py
    ├── admin.py                   # Django admin configuration
    ├── apps.py                    # App configuration
    ├── models.py                  # Database models
    ├── serializers.py             # Serializers (JSON ↔ Objects)
    ├── views.py                   # View logic (BookViewSet)
    ├── urls.py                    # App URL routing
    ├── permissions.py             # Custom permissions
    ├── filters.py                 # Custom filter sets
    ├── tests.py                   # Unit tests
    └── migrations/                # Database migrations
        └── __init__.py
```

### File Responsibilities

| File | Purpose |
|------|---------|
| **models.py** | Defines the Book table schema (title, author, category, price, published_date) |
| **serializers.py** | Handles conversion between Book objects and JSON; validates incoming data |
| **views.py** | Contains business logic - what happens for each request (GET, POST, PUT, DELETE) |
| **permissions.py** | Custom permission classes for granular access control |
| **filters.py** | Custom filter definitions for advanced querying |
| **urls.py** | Maps URL patterns to views/ViewSets |
| **settings.py** | All configuration: JWT, throttling, pagination, database, installed apps |

---

## Features

### Core Features

| Feature | Implementation | Status |
|---------|---------------|--------|
| **REST API** | Django REST Framework (ViewSets + Routers) | ✅ |
| **Book Model** | Complete with title, author, category, price, published_date | ✅ |
| **Serialization** | BookSerializer with field validation | ✅ |

### Authentication & Authorization

| Feature | Implementation | Status |
|---------|---------------|--------|
| **JWT Authentication** | Simple JWT library | ✅ |
| **Token Endpoint** | `/api/token/` - Obtain access token | ✅ |
| **Refresh Endpoint** | `/api/token/refresh/` - Refresh expired token | ✅ |
| **Protected Endpoints** | Create, Update, Delete require authentication | ✅ |
| **Public Endpoints** | View books open to everyone | ✅ |

### Query Capabilities

| Feature | Implementation | Status |
|---------|---------------|--------|
| **Filtering** | By category and author using `filterset_fields` | ✅ |
| **Searching** | By title and author using `search_fields` | ✅ |
| **Ordering** | By title, price, published_date using `ordering_fields` | ✅ |
| **Pagination** | 5 books per page (PageNumberPagination) | ✅ |
| **Throttling** | Rate limiting: 100/day for anonymous, 1000/day for users | ✅ |

### Combined Query Example

```
GET /books/?search=Python&ordering=-price&page=2
```

This single request:
- Searches books containing "Python"
- Orders results by price (highest first)
- Returns the second page of results (5 items per page)
- Applies rate limiting

---

## Installation

### Prerequisites

- Python 3.10+
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/book-management-api.git
cd book-management-api

# 2. Create and activate virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Copy environment variables
cp .env.example .env

# 5. Apply database migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser (for admin access)
python manage.py createsuperuser
# Follow prompts to create username, email, password

# 7. Load sample data (optional)
python manage.py shell
# Run the sample data creation script from docs/load_sample_data.py

# 8. Start development server
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

---

## Configuration

### Environment Variables (.env)

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for production)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60  # minutes
JWT_REFRESH_TOKEN_LIFETIME=1  # days

# Throttling
ANON_THROTTLE_RATE=100/day
USER_THROTTLE_RATE=1000/day

# Pagination
PAGE_SIZE=5
```

### Key Settings Explanation

**JWT Configuration:**
- Access tokens expire after 60 minutes (short-lived for security)
- Refresh tokens expire after 1 day (can be used to get new access tokens)
- Uses HS256 algorithm (symmetric signing)
- Tokens sent in Authorization header: `Bearer <token>`

**Throttling:**
```python
'DEFAULT_THROTTLE_RATES': {
    'anon': '100/day',   # Unauthenticated users: 100 requests/day
    'user': '1000/day'   # Authenticated users: 1000 requests/day
}
```

**Pagination:**
- 5 items per page by default
- Can be overridden with `?page_size=10` parameter
- Max page size: 100

---

## API Documentation

### Authentication Endpoints

#### 1. Obtain Token
```http
POST /api/token/
```

**Request:**
```json
{
    "username": "admin",
    "password": "secret123"
}
```

**Response:**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIs...",
    "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

#### 2. Refresh Token
```http
POST /api/token/refresh/
```

**Request:**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response:**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

### Book Endpoints

#### List All Books (Public)

```http
GET /api/books/
GET /api/books/?page=2
GET /api/books/?category=Programming
GET /api/books/?search=Python
GET /api/books/?ordering=-price
```

**Response (Paginated):**
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

#### Get Single Book (Public)

```http
GET /api/books/{id}/
```

#### Create Book (Authenticated)

```http
POST /api/books/
Authorization: Bearer <access_token>
```

**Request:**
```json
{
    "title": "Django for Professionals",
    "author": "William S. Vincent",
    "category": "Web Development",
    "price": 39.99,
    "published_date": "2023-12-01"
}
```

#### Update Book (Authenticated)

```http
PUT /api/books/{id}/      # Full update
PATCH /api/books/{id}/    # Partial update
Authorization: Bearer <access_token>
```

#### Delete Book (Authenticated)

```http
DELETE /api/books/{id}/
Authorization: Bearer <access_token>
```

---

### Query Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `category` | String | Filter by category | `?category=Programming` |
| `author` | String | Filter by author | `?author=John%20Doe` |
| `search` | String | Search across title and author | `?search=Python` |
| `ordering` | String | Order by field (prefix - for descending) | `?ordering=-price` |
| `page` | Integer | Page number for pagination | `?page=2` |
| `page_size` | Integer | Items per page (max 100) | `?page_size=10` |

---

## Testing

### Using cURL

```bash
# 1. Get Authentication Token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "secret123"}'

# 2. List Books (Public)
curl http://localhost:8000/api/books/

# 3. Create Book (Authenticated)
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

# 4. Filter by Category
curl "http://localhost:8000/api/books/?category=Programming"

# 5. Search
curl "http://localhost:8000/api/books/?search=Python"

# 6. Order by Price (Descending)
curl "http://localhost:8000/api/books/?ordering=-price"

# 7. Combined Query
curl "http://localhost:8000/api/books/?search=Python&ordering=-price&page=2"

# 8. Update Book
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

# 9. Delete Book
curl -X DELETE http://localhost:8000/api/books/1/ \
  -H "Authorization: Bearer <access_token>"
```

### Using Postman

1. Import the collection (if available in `/postman` directory)
2. Set environment variables:
   - `base_url`: http://localhost:8000
   - `access_token`: obtained from `/api/token/`
3. Test endpoints with authentication

---

## Deployment

### Production Checklist

- [ ] Change `SECRET_KEY` to strong random value
- [ ] Set `DEBUG = False`
- [ ] Update `ALLOWED_HOSTS` with production domains
- [ ] Switch to PostgreSQL/MySQL database
- [ ] Configure SSL/HTTPS
- [ ] Set up environment variables in production
- [ ] Enable logging and monitoring
- [ ] Configure CORS settings
- [ ] Run security checks: `python manage.py check --deploy`
- [ ] Set up database backups

### Deploy to Production (Example with Gunicorn + Nginx)

```bash
# 1. Install production dependencies
pip install gunicorn psycopg2-binary

# 2. Collect static files
python manage.py collectstatic --noinput

# 3. Run migrations
python manage.py migrate

# 4. Start Gunicorn
gunicorn --workers 4 --bind 0.0.0.0:8000 book_management.wsgi

# 5. Configure Nginx (example)
# /etc/nginx/sites-available/book-api
server {
    listen 80;
    server_name api.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "book_management.wsgi"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=books
      - POSTGRES_USER=books_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## Error Handling

### Common Error Responses

| Status Code | Message | When? |
|-------------|---------|-------|
| 400 Bad Request | Validation errors | Invalid data sent |
| 401 Unauthorized | "Authentication credentials were not provided." | No/invalid token |
| 403 Forbidden | "You do not have permission..." | Non-authenticated user trying write operation |
| 404 Not Found | "Not found." | Resource doesn't exist |
| 429 Too Many Requests | "Request was throttled..." | Rate limit exceeded |

### Debugging Tips

**Database Error?**
```bash
python manage.py flush  # Clear database
python manage.py migrate books zero  # Reset migrations
python manage.py makemigrations
python manage.py migrate
```

**JWT Token Issues?**
- Verify token is included in header: `Authorization: Bearer <token>`
- Check token is valid and not expired
- Use refresh endpoint to get new token

**Permission Denied?**
- Ensure user is authenticated before write operations
- Check user permissions in Django admin

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Support

For support, email your-email@example.com or create an issue in the GitHub repository.

---

**Made with ❤️ using Django REST Framework**#   B o o k _  
 #   B o o k _  
 #   b o o k A p i _ o s t a d  
 