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
   dbinit create myproject --db postgres
   ```

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

## Examples

### Using Default Path
```bash
# Creates project in configured default path
dbinit create myapp --db postgres
```

### Using Custom Path
```bash
# Creates project in specified absolute path
dbinit create /path/to/projects/myapp --db postgres
```

### Override Default Database Type
```bash
# Even if default is postgres, you can use sqlite
dbinit create myapp --db sqlite
```

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
