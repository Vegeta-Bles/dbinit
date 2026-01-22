# dbinit

Interactive database initialization tool for setting up local databases with secure credential management.

## Features

- 🎯 **Interactive Setup Wizard** - Guided configuration with numbered choices
- 🔐 **Interactive Credential Setup** - Password hiding and strength validation
- 🗄️ **Multiple Database Support** - PostgreSQL (via Docker) and SQLite
- 📁 **Automatic Project Scaffolding** - Complete project structure generation
- 🔒 **Secure Credential Storage** - Credentials stored in `.env` files (never committed)
- 🚀 **Auto-start Databases** - Automatically start PostgreSQL containers
- 🎨 **Editor Detection** - Automatically detects and lists available editors
- 🔄 **Database Upgrades** - Upgrade existing projects to new dbinit versions
- ⚙️ **Persistent Configuration** - Settings saved and remembered
- 🛡️ **Password Security** - Passwords never printed by default

## Installation

### From pip

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

## Initial Setup

After installation, run the interactive setup wizard to configure dbinit:

```bash
dbinit setup
```

This will guide you through configuring:
- Default project path (where new projects are created)
- Default database type (postgres or sqlite)
- Auto-start database option
- Docker Compose command preference
- Default editor

View your current configuration:
```bash
dbinit setup --show
```

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup instructions.

## Usage

### Create a New Database Project

The `create` command runs in fully interactive/guided mode:

```bash
dbinit create myproject
```

**Interactive Creation Process:**
1. 🗄️ **Database Type Selection** - Choose PostgreSQL or SQLite (numbered menu)
2. 🎯 Guided wizard welcomes you and shows project details
3. 🔐 Prompts for database username
4. 🔒 Prompts for password (hidden input)
5. ✅ Validates password strength
6. 🔁 Requires password confirmation
7. 📁 Generates complete project structure
8. 🚀 Starts the database (for PostgreSQL, if auto-start enabled)
9. 📝 Shows next steps and helpful commands

The interactive mode provides step-by-step guidance with numbered choices and clear feedback throughout the process.

### View Stored Credentials

```bash
dbinit creds --show myproject
```

### Upgrade Database Project

When dbinit updates, upgrade your existing database projects to the new version:

```bash
dbinit upgrade-db myproject
```

This command will:
- Detect your project's database type
- Preserve your existing credentials
- Regenerate project files with latest templates
- Update configuration files
- Mark project with current dbinit version

**Note:** Always backup your project before upgrading, especially if you have custom modifications.

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

## Commands Summary

| Command | Description |
|---------|-------------|
| `dbinit setup` | Interactive setup wizard to configure dbinit |
| `dbinit create <project>` | Create a new database project (interactive mode) |
| `dbinit creds --show <project>` | View stored database credentials |
| `dbinit upgrade-db <project>` | Upgrade existing project to current dbinit version |

## Requirements

- Python 3.7+
- Docker and Docker Compose (for PostgreSQL projects)

## Upgrade Workflow

When you update dbinit to a new version:

```bash
# 1. Upgrade dbinit
pip install --upgrade dbinit

# 2. Upgrade your existing projects
dbinit upgrade-db myproject1
dbinit upgrade-db myproject2
```

The upgrade command will:
- ✅ Preserve your credentials
- ✅ Update project files to latest templates
- ✅ Maintain your database data
- ✅ Update configuration files

## License

MIT
