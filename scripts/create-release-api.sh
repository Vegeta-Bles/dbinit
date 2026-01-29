#!/bin/bash
# Create GitHub release using API

VERSION="0.2.5"
REPO="Vegeta-Bles/dbinit"

# Release notes
RELEASE_BODY=$(cat << 'EOF'
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

\`\`\`bash
pip install dbinit==0.2.5
\`\`\`

## Upgrade

\`\`\`bash
pip install --upgrade dbinit
\`\`\`

## Full Changelog

See [CHANGELOG.md](https://github.com/Vegeta-Bles/dbinit/blob/master/CHANGELOG.md) for complete release history.
EOF
)

# Check for GitHub token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ GITHUB_TOKEN environment variable not set"
    echo ""
    echo "To create a release:"
    echo "1. Get a GitHub token from: https://github.com/settings/tokens"
    echo "2. Set it: export GITHUB_TOKEN='your-token'"
    echo "3. Run this script again"
    echo ""
    echo "Or visit: https://github.com/${REPO}/releases/new"
    exit 1
fi

echo "🚀 Creating GitHub Release v${VERSION}..."

# Create JSON payload
JSON_PAYLOAD=$(cat <<EOF
{
  "tag_name": "v${VERSION}",
  "name": "Release v${VERSION}",
  "body": $(echo "$RELEASE_BODY" | jq -Rs .),
  "draft": false,
  "prerelease": false
}
EOF
)

# Create release
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  "https://api.github.com/repos/${REPO}/releases" \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 201 ]; then
    echo "✅ Release created successfully!"
    echo "View at: https://github.com/${REPO}/releases/tag/v${VERSION}"
else
    echo "❌ Failed to create release (HTTP $HTTP_CODE)"
    echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
    exit 1
fi
