<div align="center">
  <img src="logo.png" alt="FastSchemify Logo" width="200"/>
  
  # FastSchemify
  
  > Automatically generate production-ready FastAPI REST APIs from your existing database schema. Zero boilerplate, maximum productivity.
</div>

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)

##  Overview

FastAPI Schema Generator is a powerful tool that automatically generates complete, production-ready FastAPI applications from your database. Simply connect to your database, and get a fully functional REST API with CRUD operations, automatic schema validation, and OpenAPI documentation.

### Key Features

- ⚡ **Zero Configuration** - Connect to your database and generate APIs instantly
- ⚡ **Multi-Database Support** - MySQL, PostgreSQL, MongoDB (Comming soon), and SQLite
- ⚡ **Automatic Schema Discovery** - Intelligently infers schemas from your database
- ⚡ **Full CRUD Operations** - Create, Read, Update, Delete endpoints for every table
- ⚡ **Auto-Generated Documentation** - Swagger/OpenAPI docs out of the box
- ⚡ **Production-Ready Architecture** - Clean separation of concerns with services, models, and routers
- 🔍 **Advanced Querying** - Built-in pagination, sorting, and condition-based filtering by any column
- 🔐 **JWT Authentication** - Optional Bearer token authentication for all endpoints
- ⚡ **Type-Safe** - Full type hints and Pydantic validation

##  Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/mulukenmenberu/FastSchemify.git
cd fastapi-schema-generator

# Install dependencies
pip install -r requirements.txt
```

### Generate Your First API

1. **Configure your database** by creating a `.env` file:

```env
DB_TYPE=sqlite
SQLITE_PATH=./database.db
```

2. **Generate the FastAPI project**:

```bash
python generate.py
```

3. **Run the generated API**:

```bash
cd generated_api
pip install -r requirements.txt
python app.py
```

4. **Access your API**:
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Generate API with Authentication

To generate an API with JWT Bearer token authentication:

```python
from fast_schemify import FastSchemify

# Generate API with authentication enabled
generate = FastSchemify(type='orm', output='generated_api', enable_auth=True)
generate.run()
```

When `enable_auth=True`:
- All endpoints require a Bearer token in the `Authorization` header
- Returns `401 Unauthorized` if no valid token is provided
- JWT secret key is stored in `.env` file as `JWT_SECRET_KEY`
- A `generate_sample_token.py` script is created for testing

**Configuration (.env file):**
```env
# JWT Authentication Configuration
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```

**Generate Test Tokens:**

The `generate_sample_token.py` script reads the `JWT_SECRET_KEY` from your `.env` file and generates tokens:

```bash
cd generated_api
python generate_sample_token.py
```

This will:
- Read `JWT_SECRET_KEY` from your `.env` file
- Generate both access and refresh tokens
- Display tokens with usage instructions

**Important:** Make sure `JWT_SECRET_KEY` is set in your `.env` file before running the token generator.

## 📖 Documentation

### Database Configuration

#### SQLite

```env
DB_TYPE=sqlite
SQLITE_PATH=./database.db
```

#### MySQL

```env
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
```

#### PostgreSQL

```env
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
```

#### MongoDB (comming soon)

```env
DB_TYPE=mongodb
DB_HOST=localhost
DB_PORT=27017
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password

# Or use a connection string
DB_URI=mongodb://user:password@host:port/database
```

### Generated API Structure

For each table in your database, the generator creates:

```
generated_api/
├── app.py                      # Main entry point
├── requirements.txt           # Dependencies
├── .env                       # Configuration
└── app/
    ├── main.py                # FastAPI application
    ├── core/
    │   └── config.py          # Settings management
    ├── models/                # Database models
    │   ├── database.py        # Database connection/engine
    │   ├── students.py        # SQLAlchemy ORM models (ORM mode)
    │   ├── courses.py
    │   └── ...
    ├── schemas/               # Pydantic validation schemas
    │   ├── students.py        # Request/response schemas
    │   ├── courses.py
    │   └── ...
    ├── services/              # Business logic layer
    │   ├── students_service.py
    │   ├── courses_service.py
    │   └── ...
    └── api/
        └── v1/
            └── endpoints/     # REST API endpoints
                ├── students.py
                ├── courses.py
                └── ...
```

### API Endpoints

Each table automatically gets these endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/{table}/` | List all items (paginated, filterable) |
| `GET` | `/api/v1/{table}/{id}` | Get single item |
| `POST` | `/api/v1/{table}/` | Create new item |
| `PUT` | `/api/v1/{table}/{id}` | Full update |
| `PATCH` | `/api/v1/{table}/{id}` | Partial update |
| `DELETE` | `/api/v1/{table}/{id}` | Delete item |
| `GET` | `/api/v1/{table}/count/total` | Get total count |

### Query Parameters

All list endpoints (`GET /api/v1/{table}/`) support:

- `skip` - Number of items to skip (default: 0)
- `limit` - Maximum items to return (default: 100, max: 1000)
- `sort_by` - Column name to sort by
- `order` - Sort direction: `asc` or `desc` (default: `asc`)

### Filtering

**Condition-based filtering** is available on all list endpoints. You can filter by any column in the table by passing the column name as a query parameter.

**How it works:**
- Pass any column name as a query parameter with its value
- Multiple filters are combined with `AND` logic
- Only valid column names are accepted (invalid columns are ignored)
- Filtering works alongside pagination and sorting

**Filtering Examples:**

```bash
# Filter by a single column
curl "http://localhost:8000/api/v1/courses/?course_name=Mathematics"

# Filter by multiple columns (AND logic)
curl "http://localhost:8000/api/v1/courses/?course_name=Physics&teacher_id=2"

# Filter students by email
curl "http://localhost:8000/api/v1/students/?email=alice@example.com"

# Combine filtering with pagination and sorting
curl "http://localhost:8000/api/v1/courses/?teacher_id=1&limit=10&sort_by=course_name&order=asc"

# Filter by date (if your table has date columns)
curl "http://localhost:8000/api/v1/students/?enrollment_date=2025-01-01"
```

**Note:** Filter values are matched exactly (equality). For more complex filtering (range queries, LIKE, etc.), you can extend the generated service layer.

### Authentication

When `enable_auth=True` is set during generation, all endpoints require JWT Bearer token authentication.

**How it works:**
- All API endpoints require a valid Bearer token in the `Authorization` header
- Returns `401 Unauthorized` if token is missing or invalid
- JWT secret key must be stored in `.env` file as `JWT_SECRET_KEY`
- Token generation script (`generate_sample_token.py`) is created for testing

**Configuration:**

Add to your `.env` file:
```env
JWT_SECRET_KEY=your-secret-key-here-min-32-chars
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```

**Generate Test Tokens:**

```bash
cd generated_api
python generate_sample_token.py
```

This script will:
- Read `JWT_SECRET_KEY` from your `.env` file
- Generate both access and refresh tokens
- Display tokens with usage instructions

**Using Tokens:**

```bash
# Make authenticated requests
curl -H "Authorization: Bearer <ACCESS_TOKEN>" \\
  "http://localhost:8000/api/v1/courses/"

# Example with token
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \\
  "http://localhost:8000/api/v1/students/?first_name=Alice"
```

**Note:** The `generate_sample_token.py` script creates sample tokens for testing. In production, implement a proper login endpoint that generates tokens after user authentication.

### Example Usage

```bash
# Get all items with pagination
curl "http://localhost:8000/api/v1/users/?skip=0&limit=10&sort_by=created_at&order=desc"

# Filter by column value
curl "http://localhost:8000/api/v1/courses/?course_name=Mathematics"

# Multiple filters combined with AND
curl "http://localhost:8000/api/v1/students/?first_name=Alice&email=alice@example.com"

# Combine filtering, pagination, and sorting
curl "http://localhost:8000/api/v1/courses/?teacher_id=1&limit=10&sort_by=course_name&order=asc"

# Get user by ID
curl "http://localhost:8000/api/v1/users/1"

# Create a new user
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'

# Update user
curl -X PUT "http://localhost:8000/api/v1/users/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe", "email": "jane@example.com"}'

# Delete user
curl -X DELETE "http://localhost:8000/api/v1/users/1"
```

## 🏗️ Architecture

The generated projects follow industry best practices:

- **Separation of Concerns**: Models, Services, and Routes are cleanly separated
- **Service Layer**: Business logic lives in services, not in routes
- **Type Safety**: Full type hints with Pydantic models
- **Dependency Injection**: Ready for dependency injection patterns
- **Error Handling**: Proper HTTP status codes and error messages

## 🔧 How It Works

1. **Connect** to your database using the configured settings
2. **Discover** all tables/collections and their schemas automatically
3. **Generate** REST API endpoints for each table
4. **Create** Pydantic models dynamically based on database schema
5. **Implement** full CRUD operations with proper validation

## 🗄️ Database Support

### SQL Databases (MySQL, PostgreSQL, SQLite)

- Automatic primary key detection
- Foreign key relationship awareness
- Column type inference
- Transaction support
- SQLAlchemy ORM integration

### MongoDB

- Schema inference from sample documents
- Automatic ObjectId handling
- Collection-based operations
- Flexible document structure support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and follow the existing code style.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Database support via [SQLAlchemy](https://www.sqlalchemy.org/)
- Schema validation with [Pydantic](https://docs.pydantic.dev/)

## 📧 Support

For issues, questions, or contributions, please open an issue on [GitHub](https://github.com/mulukenmenberu/FastSchemify/issues).

---

Made with ❤️ for the FastAPI community
