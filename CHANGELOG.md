# Changelog

All notable changes to dbinit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.5] - 2025-01-28

### Added
- Docker detection and installation warnings
- Quick connect helper (`dbinit.connect()`) for easy database connections
- Connection helper functions: `get_sqlite_connection()`, `get_postgres_connection_string()`
- Comprehensive connection examples in SETUP_GUIDE.md
- SQLite database file location information in project output

### Changed
- Removed `--db` command-line option (now fully interactive)
- Enhanced "Next Steps" output to show SQLite database file location
- Improved Docker warnings with platform-specific installation commands
- Updated README generation with quick connect examples

### Fixed
- "Database is already running" message now only shows when Docker is installed
- Better handling of missing Docker during project creation

## [0.2.4] - 2025-01-19

### Changed
- Removed `--db` command-line option from `create` command
- Made database type selection fully interactive with numbered menu
- Simplified command: `dbinit create myproject` (no flags needed)

### Added
- Interactive database type selection at start of project creation
- Build and publish automation scripts
- PyPI environment variable setup

## [0.2.3] - 2025-01-19

### Added
- Interactive guided mode for `dbinit create` command
- `dbinit upgrade-db` command to upgrade existing projects
- Version tracking with `.dbinit-version` files
- Step-by-step wizard with visual feedback

### Changed
- Enhanced project creation with step-by-step guidance
- Improved user experience with emojis and clear sections
- Updated README with new features and upgrade workflow

## [0.2.2] - 2025-01-19

### Added
- Interactive setup wizard with numbered choices
- Editor detection and automatic selection
- Database creation option during setup
- Configuration persistence in `~/.dbinit/config.json`

### Changed
- Setup wizard now uses numbered menus instead of text input
- Docker Compose command selection with numbered options
- Editor selection with automatic detection

## [0.2.1] - 2025-01-19

### Changed
- Made `--db` option optional, uses configured default
- Improved configuration handling

## [0.2.0] - 2025-01-19

### Added
- Interactive setup wizard (`dbinit setup`)
- Configuration system with persistent settings
- Default project path configuration
- Default database type preference
- Auto-start database toggle
- Docker Compose command preference
- Default editor configuration
- Auto-run setup script for terminal initialization

### Changed
- Projects now use configured default path
- Docker Compose command respects user preference
- Auto-start behavior is configurable

## [0.1.1] - 2025-01-19

### Added
- Initial PyPI release

## [0.1.0] - 2025-01-19

### Added
- Initial release
- Interactive credential setup with password hiding
- Password strength validation
- Support for PostgreSQL (via Docker) and SQLite
- Automatic project scaffolding
- Secure credential storage in `.env` files
- Docker Compose integration for PostgreSQL
- Project structure generation (docker-compose.yml, .env, .gitignore, migrations/, README.md)
- Credential viewing command (`dbinit creds --show`)

[Unreleased]: https://github.com/Vegeta-Bles/dbinit/compare/v0.2.5...HEAD
[0.2.5]: https://github.com/Vegeta-Bles/dbinit/compare/v0.2.4...v0.2.5
[0.2.4]: https://github.com/Vegeta-Bles/dbinit/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/Vegeta-Bles/dbinit/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/Vegeta-Bles/dbinit/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/Vegeta-Bles/dbinit/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/Vegeta-Bles/dbinit/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/Vegeta-Bles/dbinit/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/Vegeta-Bles/dbinit/releases/tag/v0.1.0
