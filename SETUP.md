# Setup Guide

This guide will help you set up FastAPI Schema Generator for development or production use.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Access to a database (MySQL, PostgreSQL, MongoDB, or SQLite)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fastapi-schema-generator.git
cd fastapi-schema-generator
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Create Environment File

Copy the example environment file:

```bash
cp .env.example .env
```

### 2. Configure Database

Edit `.env` file with your database credentials. See [README.md](README.md) for configuration examples for each database type.

## Usage

### Generate a FastAPI Project

```bash
python generate.py
```

This will create a `generated_api` directory with a complete FastAPI project.

### Run the Generated API

```bash
cd generated_api
pip install -r requirements.txt
python app.py
```

The API will be available at http://localhost:8000

## Development

### Project Structure

```
fastapi-schema-generator/
├── api/                 # API generation logic
├── database/            # Database connection handlers
├── generate.py         # Main generator script
├── config.py           # Configuration management
└── requirements.txt    # Python dependencies
```

### Running Tests

Currently, manual testing is recommended. Test the generator with different database types:

1. Set up a test database
2. Configure `.env` file
3. Run `python generate.py`
4. Test the generated API endpoints

## Troubleshooting

### Database Connection Issues

- Verify database credentials in `.env`
- Ensure database server is running
- Check network connectivity for remote databases
- For SQLite, verify file path is correct

### Import Errors

- Ensure virtual environment is activated
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

### Generated API Issues

- Check that database file exists (for SQLite)
- Verify table names match your database schema
- Review error messages in the generated API logs

## Next Steps

- Read the [README.md](README.md) for detailed usage instructions
- Check [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute
- Review generated API documentation at http://localhost:8000/docs

