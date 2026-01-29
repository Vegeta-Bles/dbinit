#!/bin/bash
# Create a GitHub release for dbinit

set -e

VERSION="0.2.5"
REPO="Vegeta-Bles/dbinit"

# Get release notes from CHANGELOG
RELEASE_NOTES=$(cat << 'EOF'
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
EOF
)

echo "🚀 Creating GitHub Release v${VERSION}..."
echo ""

# Check if GitHub CLI is available
if command -v gh &> /dev/null; then
    echo "Using GitHub CLI..."
    gh release create "v${VERSION}" \
        --title "Release v${VERSION}" \
        --notes "$RELEASE_NOTES" \
        --repo "$REPO"
    echo ""
    echo "✅ Release created successfully!"
    echo "View at: https://github.com/${REPO}/releases/tag/v${VERSION}"
else
    echo "GitHub CLI not found. Creating release via API..."
    echo ""
    echo "To create the release, you can:"
    echo ""
    echo "1. Visit: https://github.com/${REPO}/releases/new"
    echo "2. Select tag: v${VERSION}"
    echo "3. Title: Release v${VERSION}"
    echo "4. Description:"
    echo ""
    echo "$RELEASE_NOTES"
    echo ""
    echo "Or install GitHub CLI and run this script again:"
    echo "  brew install gh  # macOS"
    echo "  gh auth login"
    echo ""
    echo "Or use curl with a GitHub token:"
    echo "  export GITHUB_TOKEN='your-token'"
    echo "  curl -X POST https://api.github.com/repos/${REPO}/releases \\"
    echo "    -H \"Authorization: token \$GITHUB_TOKEN\" \\"
    echo "    -H \"Content-Type: application/json\" \\"
    echo "    -d '{\"tag_name\":\"v${VERSION}\",\"name\":\"Release v${VERSION}\",\"body\":\"...\"}'"
fi
