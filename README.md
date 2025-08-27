# Personal Blog Platform API

A comprehensive RESTful API for a personal blogging platform with user authentication, role-based access control, and full CRUD operations for posts, comments, and categories.

## Features

### User Management
- ✅ User registration and login with JWT authentication
- ✅ Password hashing with bcrypt
- ✅ Role-based access control (Admin/User)
- ✅ Profile management

### Blog Posts
- ✅ Full CRUD operations for posts
- ✅ Posts belong to categories and authors
- ✅ Only authors can edit/delete their posts (admins can manage all)
- ✅ Pagination and search functionality

### Comments
- ✅ Users can comment on posts
- ✅ CRUD operations for comments
- ✅ Users can edit/delete their own comments

### Categories
- ✅ Category management (Admin only)
- ✅ Posts must belong to a category

### Security & Features
- ✅ Input validation and sanitization
- ✅ Proper HTTP status codes
- ✅ Error handling middleware
- ✅ Search by title, content, or category
- ✅ Pagination for all list endpoints

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd personal-blog-platform
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set environment variables** (optional)
Create a `.env` file:
```
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///blog.db
```

5. **Run the application**
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## Default Test Credentials

The application creates a default admin user on first run:
- **Username:** `admin`
- **Email:** `admin@example.com`
- **Password:** `admin123`
- **Role:** `admin`

**⚠️ Important:** Change the default admin password in production!

## API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "password123"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "role": "user",
    "created_at": "2024-01-15T10:30:00"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Login
```http
POST /api/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "role": "user",
    "created_at": "2024-01-15T10:30:00"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Get Profile
```http
GET /api/profile
Authorization: Bearer <your-jwt-token>
```

### Category Endpoints

#### Get All Categories
```http
GET /api/categories
```

**Response (200 OK):**
```json
{
  "categories": [
    {
      "id": 1,
      "name": "Technology",
      "description": "Tech-related posts",
      "created_at": "2024-01-15T10:30:00",
      "post_count": 5
    }
  ]
}
```

#### Create Category (Admin Only)
```http
POST /api/categories
Authorization: Bearer <admin-jwt-token>
Content-Type: application/json

{
  "name": "Travel",
  "description": "Travel experiences and tips"
}
```

#### Update Category (Admin Only)
```http
PUT /api/categories/{id}
Authorization: Bearer <admin-jwt-token>
Content-Type: application/json

{
  "name": "Updated Category Name",
  "description": "Updated description"
}
```

#### Delete Category (Admin Only)
```http
DELETE /api/categories/{id}
Authorization: Bearer <admin-jwt-token>
```

### Post Endpoints

#### Get All Posts (with pagination and search)
```http
GET /api/posts?page=1&per_page=10&search=python&category=1&author=2
```

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `per_page` (int): Items per page (default: 10, max: 100)
- `search` (string): Search in title and content
- `category` (int): Filter by category ID
- `author` (int): Filter by author ID

**Response (200 OK):**
```json
{
  "posts": [
    {
      "id": 1,
      "title": "Getting Started with Python",
      "content": "Python is a powerful programming language...",
      "author": {
        "id": 1,
        "username": "johndoe"
      },
      "category": {
        "id": 1,
        "name": "Technology"
      },
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00",
      "comment_count": 3
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 25,
    "pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

#### Get Single Post
```http
GET /api/posts/{id}
```

#### Create Post
```http
POST /api/posts
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "title": "My Awesome Blog Post",
  "content": "This is the content of my blog post...",
  "category_id": 1
}
```

#### Update Post (Author or Admin only)
```http
PUT /api/posts/{id}
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content...",
  "category_id": 2
}
```

#### Delete Post (Author or Admin only)
```http
DELETE /api/posts/{id}
Authorization: Bearer <your-jwt-token>
```

### Comment Endpoints

#### Get Comments for a Post
```http
GET /api/posts/{post_id}/comments?page=1&per_page=20
```

**Response (200 OK):**
```json
{
  "comments": [
    {
      "id": 1,
      "content": "Great post! Very informative.",
      "author": {
        "id": 2,
        "username": "jane"
      },
      "post_id": 1,
      "created_at": "2024-01-15T11:30:00",
      "updated_at": "2024-01-15T11:30:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 5,
    "pages": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

#### Create Comment
```http
POST /api/posts/{post_id}/comments
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "content": "This is my comment on the post."
}
```

#### Update Comment (Author or Admin only)
```http
PUT /api/comments/{id}
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "content": "Updated comment content."
}
```

#### Delete Comment (Author or Admin only)
```http
DELETE /api/comments/{id}
Authorization: Bearer <your-jwt-token>
```

### Admin Endpoints

#### Get All Users (Admin Only)
```http
GET /api/admin/users?page=1&per_page=20
Authorization: Bearer <admin-jwt-token>
```

#### Update User Role (Admin Only)
```http
PUT /api/admin/users/{user_id}/role
Authorization: Bearer <admin-jwt-token>
Content-Type: application/json

{
  "role": "admin"
}
```

### Health Check
```http
GET /api/health
```

## Error Responses

The API returns consistent error responses:

```json
{
  "error": "Error message describing what went wrong"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (authentication required)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `500` - Internal Server Error

## Example Usage with curl

### 1. Register a new user
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 2. Login and get token
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### 3. Create a post (replace TOKEN with your JWT)
```bash
curl -X POST http://localhost:5000/api/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "title": "My First Post",
    "content": "This is my first blog post!",
    "category_id": 1
  }'
```

### 4. Get all posts with search
```bash
curl "http://localhost:5000/api/posts?search=python&page=1&per_page=5"
```

### 5. Add a comment to a post
```bash
curl -X POST http://localhost:5000/api/posts/1/comments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "content": "Great post! Thanks for sharing."
  }'
```

## Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email address
- `password_hash` - Bcrypt hashed password
- `role` - User role ('user' or 'admin')
- `created_at` - Account creation timestamp

### Categories Table
- `id` - Primary key
- `name` - Unique category name
- `description` - Category description
- `created_at` - Creation timestamp

### Posts Table
- `id` - Primary key
- `title` - Post title
- `content` - Post content
- `author_id` - Foreign key to users table
- `category_id` - Foreign key to categories table
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### Comments Table
- `id` - Primary key
- `content` - Comment content
- `author_id` - Foreign key to users table
- `post_id` - Foreign key to posts table
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

## Deployment Options

### Option 1: Render (Free)
1. Create account at [render.com](https://render.com)
2. Connect your GitHub repository
3. Create a new Web Service
4. Set environment variables in Render dashboard
5. Deploy!

### Option 2: Railway (Free tier)
1. Create account at [railway.app](https://railway.app)
2. Connect GitHub repository
3. Add environment variables
4. Deploy with one click

### Option 3: Replit
1. Import from GitHub to [replit.com](https://replit.com)
2. Install dependencies with `pip install -r requirements.txt`
3. Run the application

## Environment Variables for Production

```bash
SECRET_KEY=your-super-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-change-this
DATABASE_URL=sqlite:///blog.db  # or PostgreSQL URL for production
```

## Security Considerations

1. **Change default admin credentials** immediately after first deployment
2. **Use strong secrets** for JWT and Flask secret keys
3. **Use HTTPS** in production
4. **Use PostgreSQL** instead of SQLite for production
5. **Implement rate limiting** for API endpoints
6. **Add input sanitization** for user-generated content
7. **Regular security updates** for dependencies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions, please:
1. Check the existing GitHub issues
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

---

**Happy Blogging! 🎉**