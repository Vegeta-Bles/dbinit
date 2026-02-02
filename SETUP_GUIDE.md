# dbinit Setup Guide

## Quick Start

1. **Install dbinit:**
   ```bash
   pip install dbinit
   ```

2. **Run the setup wizard:**
   ```bash
   dbinit setup
   ```

3. **Create your first project:**
   ```bash
   dbinit create myproject
   ```
   (You'll be prompted to select PostgreSQL or SQLite)

## Configuration Options

The setup wizard configures the following settings:

### 1. Default Project Path
Where new database projects will be created by default.
- Default: `~/projects` (if exists) or current directory
- Projects can still be created in any location by using absolute paths

### 2. Default Database Type
Your preferred database type (postgres or sqlite).
- This sets the default, but you can override with `--db` flag

### 3. Auto-start Database
Whether to automatically start PostgreSQL containers after creation.
- Enabled by default
- Can be disabled if you prefer manual control

### 4. Docker Compose Command
Which command to use for Docker Compose.
- Options: `docker-compose` (v1) or `docker compose` (v2)
- Default: `docker-compose`

### 5. Default Editor
Editor command for opening project files.
- Defaults to `$EDITOR` environment variable or `nano`

## Configuration File Location

All settings are stored in: `~/.dbinit/config.json`

You can edit this file directly or run `dbinit setup` again to update settings.

## View Current Configuration

```bash
dbinit setup --show
```

## Auto-run Setup on Terminal Open

If you want dbinit to automatically prompt for setup when you open a new terminal (only if not configured), add this to your shell profile:

### For Bash
Add to `~/.bashrc` or `~/.bash_profile`:
```bash
# Auto-run dbinit setup if not configured
if [ -f ~/.dbinit/scripts/dbinit-setup.sh ]; then
    source ~/.dbinit/scripts/dbinit-setup.sh
fi
```

### For Zsh
Add to `~/.zshrc`:
```bash
# Auto-run dbinit setup if not configured
if [ -f ~/.dbinit/scripts/dbinit-setup.sh ]; then
    source ~/.dbinit/scripts/dbinit-setup.sh
fi
```

**Note:** The script will only prompt if configuration doesn't exist, so it won't interrupt you after initial setup.

## Connecting to Your Database

### Quick Connect (Recommended)

```python
import dbinit

conn = dbinit.connect()  # Returns ready-to-use connection
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
conn.close()
```

**Get Connection Info (if you need details without connecting):**
```python
import dbinit

# Get connection info object (doesn't actually connect)
conn_info = dbinit.get_connection_info_obj()

db_path = conn_info.db_path        # Full path to SQLite database file (e.g., '/path/to/test.db')
db_username = conn_info.db_username  # Database username from .env file
db_password = conn_info.db_password  # Database password from .env file
db_name = conn_info.db_name         # Database name (e.g., 'test.db' for SQLite)
db_type = conn_info.db_type          # Database type: 'sqlite' or 'postgres'
```

**For PostgreSQL:**
```python
import dbinit
import psycopg2

conn_info = dbinit.connect()
conn_string = dbinit.get_postgres_connection_string()

# Use with psycopg2
conn = psycopg2.connect(conn_string)
```

### SQLite Database Connection (Manual)

SQLite databases are created automatically when you first connect to them. The database file will be created in your project root directory.

**Using Python (sqlite3):**
```python
import sqlite3
import os
from pathlib import Path
from dotenv import load_dotenv  # pip install python-dotenv

# Load .env file
load_dotenv()

# Get database path from .env
db_name = os.getenv("DB_NAME", "test.db")
db_path = Path(".") / db_name

# Connect to SQLite (no username/password required)
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Example: Create a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
""")

# Example: Insert data
cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)", 
               ("John Doe", "john@example.com"))

# Example: Query data
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

# Commit and close
conn.commit()
conn.close()
```

**Using Command Line:**
```bash
# Navigate to your project directory
cd myproject

# Connect to SQLite database
sqlite3 myproject.db

# In sqlite3 prompt:
.tables          # List all tables
.schema          # Show database schema
SELECT * FROM users;
.quit            # Exit
```

**Note:** SQLite doesn't enforce username/password authentication. The credentials stored in `.env` are for reference and consistency with PostgreSQL projects.

### PostgreSQL Database Connection

**Using Python (psycopg2):**
```python
import os
import psycopg2
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get connection details from .env
conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()
cursor.execute("SELECT version();")
print(cursor.fetchone())
conn.close()
```

**Using Command Line (psql):**
```bash
# Navigate to your project directory
cd myproject

# Load environment variables
export $(cat .env | xargs)

# Connect using psql
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME

# Or connect directly
psql postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME
```

**Using Connection String:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Build connection string
conn_string = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Use with your database library
```

## Working with Your Database

### SQLite - Terminal Commands

**Connect to your database:**
```bash
cd myproject
sqlite3 myproject.db
```

**Create a table:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Insert data:**
```sql
-- Insert a single row
INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');

-- Insert multiple rows
INSERT INTO users (name, email) VALUES 
    ('Jane Smith', 'jane@example.com'),
    ('Bob Johnson', 'bob@example.com');
```

**Query data:**
```sql
-- Select all rows
SELECT * FROM users;

-- Select specific columns
SELECT name, email FROM users;

-- Select with conditions
SELECT * FROM users WHERE email = 'john@example.com';

-- Count rows
SELECT COUNT(*) FROM users;
```

**Update data:**
```sql
UPDATE users SET email = 'john.doe@example.com' WHERE id = 1;
```

**Delete data:**
```sql
DELETE FROM users WHERE id = 1;
```

**Useful SQLite commands:**
```sql
.tables          # List all tables
.schema          # Show database schema
.schema users    # Show schema for specific table
.headers on      # Show column headers in SELECT results
.mode column     # Display results in column format
.quit            # Exit sqlite3
```

### PostgreSQL - Terminal Commands

**Connect to your database:**
```bash
cd myproject
export $(cat .env | xargs)
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME
```

**Create a table:**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Insert data:**
```sql
-- Insert a single row
INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');

-- Insert multiple rows
INSERT INTO users (name, email) VALUES 
    ('Jane Smith', 'jane@example.com'),
    ('Bob Johnson', 'bob@example.com');
```

**Query data:**
```sql
-- Select all rows
SELECT * FROM users;

-- Select specific columns
SELECT name, email FROM users;

-- Select with conditions
SELECT * FROM users WHERE email = 'john@example.com';

-- Count rows
SELECT COUNT(*) FROM users;
```

**Update data:**
```sql
UPDATE users SET email = 'john.doe@example.com' WHERE id = 1;
```

**Delete data:**
```sql
DELETE FROM users WHERE id = 1;
```

**Useful PostgreSQL commands:**
```sql
\dt              # List all tables
\d users         # Describe table structure
\l               # List all databases
\c database_name # Connect to a different database
\q               # Exit psql
```

### Python Examples

**Create table and insert data:**
```python
import dbinit

conn = dbinit.connect()
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
""")

# Insert data
cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", 
               ("John Doe", "john@example.com"))

# Insert multiple rows
users = [
    ("Jane Smith", "jane@example.com"),
    ("Bob Johnson", "bob@example.com")
]
cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users)

# Commit changes
conn.commit()

# Query data
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
```

### Using dbinit CLI Commands

**Add a row to a table:**
```bash
# Navigate to your project directory (or use project name)
cd myproject

# Add a row using key=value pairs
dbinit add-row myproject users name="John Doe" email="john@example.com"

# Add multiple columns at once
dbinit add-row myproject users name="Jane Smith" email="jane@example.com" age=30

# Works with both SQLite and PostgreSQL projects
```

**Note:** The `add-row` command automatically:
- Connects to your database using credentials from `.env`
- Validates the table exists
- Inserts the data with proper escaping
- Handles both SQLite and PostgreSQL syntax

### Using Environment Variables

All database credentials are stored in the `.env` file. Load them in your application:

**Python:**
```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env file

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
```

**Shell/Bash:**
```bash
# Load all variables
export $(cat .env | xargs)

# Or load individually
source <(grep -v '^#' .env | sed 's/^/export /')
```

## Examples

### Using Default Path
```bash
# Creates project in configured default path
# You'll be prompted to select database type (PostgreSQL or SQLite)
dbinit create myapp
```

### Using Custom Path
```bash
# Creates project in specified absolute path
dbinit create /path/to/projects/myapp
```

### Database Type Selection
When you run `dbinit create`, you'll be shown a numbered menu to select:
- PostgreSQL (via Docker)
- SQLite

Your configured default will be pre-selected, but you can choose either option.

## Troubleshooting

### Configuration Not Found
If you get errors about missing configuration, run:
```bash
dbinit setup
```

### Reset Configuration
To reset all settings:
```bash
rm ~/.dbinit/config.json
dbinit setup
```

### View Configuration File
```bash
cat ~/.dbinit/config.json
```
