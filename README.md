# Backend FastAPI Practice

This project is a practice REST API built with FastAPI and Python. It provides a
CRUD service for products stored in memory, including filtering by category,
name search, pagination, and data validation with Pydantic.

Because the products are stored in memory, any products created, updated, or
deleted through the API are reset when the server restarts.

## Requirements

- Python 3.14 or later
- Git
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Installation

Clone the repository and move into the project directory:

```bash
git clone https://github.com/Envy528/Riwi-Backend-FastAPI-Test.git
cd Riwi-Backend-FastAPI-Test
```

Install the project dependencies and create the virtual environment with `uv`:

```bash
uv sync
```

## Run the API

Start the FastAPI development server from the project root:

```bash
uv run fastapi dev src/backend_fastapi/main.py
```

The API will be available at:

- http://127.0.0.1:8000/products
- Interactive Swagger UI: http://127.0.0.1:8000/docs
- ReDoc documentation: http://127.0.0.1:8000/redoc

Use the interactive documentation in `/docs` to test the product endpoints.
