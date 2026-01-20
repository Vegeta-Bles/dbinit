# dbinit

Interactive database initialization tool for setting up local databases with secure credential management.

## Features

- Interactive credential setup with password hiding
- Password strength validation
- Support for PostgreSQL (via Docker) and SQLite
- Automatic project scaffolding
- Secure credential storage in `.env` files
- Never prints passwords by default

## Installation

### From PyPI (when published)

```bash
pip install dbinit
```

### From Source

Clone the repository and install:

```bash
# Regular installation
pip install .

# Or editable/development installation
pip install -e .
```

### Development Setup

```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

### Create a New Database Project

```bash
# PostgreSQL project
dbinit create myproject --db postgres

# SQLite project
dbinit create myproject --db sqlite
```

The tool will:
1. Prompt for database username
2. Prompt for password (hidden input)
3. Validate password strength
4. Require password confirmation
5. Generate project structure
6. Start the database (for PostgreSQL)

### View Stored Credentials

```bash
dbinit creds --show myproject
```

## Project Structure

When you create a project, the following structure is generated:

```
myproject/
├── docker-compose.yml  # PostgreSQL configuration (Postgres only)
├── .env                # Database credentials (never committed)
├── .gitignore          # Git ignore rules
├── migrations/         # Database migrations directory
└── README.md           # Project documentation
```

## Password Requirements

Passwords must meet the following criteria:
- At least 8 characters long
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)

## Security

- Passwords are never printed to the console by default
- Credentials are stored in `.env` files (automatically gitignored)
- Use `dbinit creds --show` to view credentials when needed
- Never commit `.env` files to version control

## Requirements

- Python 3.7+
- Docker and Docker Compose (for PostgreSQL projects)

## License

MIT
