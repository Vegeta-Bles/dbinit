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

## Troubleshooting

**`dbinit create` puts projects in an unexpected directory**
- If you pass a relative project name (e.g., `dbinit create myproject`), dbinit uses the configured default project path from `~/.dbinit/config.json`.
- Run `dbinit setup --show` to confirm the saved default path, or re-run `dbinit setup` to update it.

**Auto-start fails for PostgreSQL**
- dbinit uses the configured Docker Compose command (`docker compose` v2 or `docker-compose` v1). If the wrong command is configured, re-run `dbinit setup` and pick the other option.
- If Docker isn't running, `docker compose up -d` will fail—start Docker Desktop or your daemon and retry.
- If auto-start is disabled, dbinit prints the manual command to run in the generated project directory.

**"docker-compose not found" warning**
- This means the configured compose command isn't available on your PATH. Install Docker Compose or switch to the alternative command in `dbinit setup`.

**Permissions errors when creating a project**
- dbinit writes to the configured default project path and creates a `.env` file plus `docker-compose.yml` (PostgreSQL). Ensure the target directory is writable, or choose a new path in `dbinit setup`.

**`dbinit upgrade-db` can't find my project**
- If you created the project with a relative name, dbinit looks in the default project path (`~/.dbinit/config.json`). Either run the command from an absolute path (e.g., `dbinit upgrade-db /full/path/myproject`) or update the default path in setup.

## Release Process

To create a new release:

```bash
./scripts/release.sh
```

The release script will:
1. ✅ Prompt for new version number
2. ✅ Update version in all files
3. ✅ Build the package
4. ✅ Create git commit and tag
5. ✅ Optionally push to GitHub
6. ✅ Optionally publish to PyPI

## Publishing to PyPI

For maintainers, to publish new versions:

### Setup (one-time)

1. **Set up environment variables:**
   ```bash
   # Option 1: Use the setup script (recommended)
   source scripts/setup-pypi-env.sh
   
   # Option 2: Set manually
   export TWINE_API_TOKEN='your-pypi-api-token'
   export TWINE_USERNAME='__token__'
   ```

2. **Or add to your shell profile** (`~/.zshrc` or `~/.bashrc`):
   ```bash
   export TWINE_API_TOKEN='your-pypi-api-token'
   export TWINE_USERNAME='__token__'
   ```

### Build and Publish

```bash
# Build only
./scripts/build-and-publish.sh

# Build and publish to PyPI
./scripts/build-and-publish.sh --publish
```

The script will:
- Clean previous builds
- Build the package
- Check the package
- Publish to PyPI (if `--publish` flag is used)

## License

MIT
