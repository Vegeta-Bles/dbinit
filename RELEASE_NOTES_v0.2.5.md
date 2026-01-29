# Release v0.2.5

## What's New in v0.2.5

### ✨ New Features
- **Docker Detection**: Automatic detection with platform-specific installation warnings
- **Quick Connect Helper**: Easy database connections with `dbinit.connect()`
- **Connection Helpers**: `get_sqlite_connection()` and `get_postgres_connection_string()`

### 🔄 Changes
- Removed `--db` option - database selection is now fully interactive
- Enhanced SQLite database location information in project output
- Improved Docker warnings with installation commands for your platform

### 🐛 Fixes
- "Database is already running" message now only shows when Docker is installed
- Better handling of missing Docker during project creation

### 📚 Documentation
- Comprehensive connection examples in SETUP_GUIDE.md
- Quick connect examples in generated READMEs

## Installation

```bash
pip install dbinit==0.2.5
```

## Upgrade

```bash
pip install --upgrade dbinit
```

## Full Changelog

See [CHANGELOG.md](https://github.com/Vegeta-Bles/dbinit/blob/master/CHANGELOG.md) for complete release history.
