#!/bin/bash
# Release script for dbinit
# This script helps create a new release

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get current version
CURRENT_VERSION=$(grep -E "version=\"[0-9]+\.[0-9]+\.[0-9]+\"" setup.py | sed -E 's/.*version="([^"]+)".*/\1/')

echo -e "${BLUE}🚀 dbinit Release Script${NC}"
echo -e "${BLUE}=======================${NC}\n"

echo -e "Current version: ${GREEN}${CURRENT_VERSION}${NC}\n"

# Ask for new version
read -p "Enter new version (e.g., 0.2.5): " NEW_VERSION

if [ -z "$NEW_VERSION" ]; then
    echo -e "${RED}❌ Version cannot be empty${NC}"
    exit 1
fi

# Validate version format
if ! [[ "$NEW_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}❌ Invalid version format. Use semantic versioning (e.g., 0.2.5)${NC}"
    exit 1
fi

echo -e "\n${YELLOW}📝 Release Notes${NC}"
echo -e "${YELLOW}===============${NC}"
read -p "Enter release notes (one line summary): " RELEASE_NOTES

if [ -z "$RELEASE_NOTES" ]; then
    RELEASE_NOTES="Release version ${NEW_VERSION}"
fi

echo -e "\n${BLUE}📋 Release Summary${NC}"
echo -e "${BLUE}=================${NC}"
echo -e "  Version: ${GREEN}${NEW_VERSION}${NC}"
echo -e "  Current: ${CURRENT_VERSION}"
echo -e "  Notes: ${RELEASE_NOTES}"
echo ""

read -p "Continue with release? (y/N): " CONFIRM

if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Release cancelled.${NC}"
    exit 0
fi

echo -e "\n${BLUE}🔄 Updating version numbers...${NC}"

# Update version in setup.py
sed -i '' "s/version=\"${CURRENT_VERSION}\"/version=\"${NEW_VERSION}\"/" setup.py

# Update version in __init__.py
sed -i '' "s/__version__ = \"${CURRENT_VERSION}\"/__version__ = \"${NEW_VERSION}\"/" dbinit/__init__.py

# Update version in cli.py
sed -i '' "s/@click.version_option(version=\"${CURRENT_VERSION}\")/@click.version_option(version=\"${NEW_VERSION}\")/" dbinit/cli.py

echo -e "${GREEN}✓ Version numbers updated${NC}"

# Verify version updates
echo -e "\n${BLUE}🔍 Verifying version updates...${NC}"
if grep -q "version=\"${NEW_VERSION}\"" setup.py && \
   grep -q "__version__ = \"${NEW_VERSION}\"" dbinit/__init__.py && \
   grep -q "@click.version_option(version=\"${NEW_VERSION}\")" dbinit/cli.py; then
    echo -e "${GREEN}✓ All version numbers updated correctly${NC}"
else
    echo -e "${RED}❌ Version update verification failed${NC}"
    exit 1
fi

# Build the package
echo -e "\n${BLUE}🔨 Building package...${NC}"
./scripts/build-and-publish.sh

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi

# Commit changes
echo -e "\n${BLUE}📝 Committing changes...${NC}"
git add setup.py dbinit/__init__.py dbinit/cli.py CHANGELOG.md

# Check if there are uncommitted changes
if ! git diff --staged --quiet; then
    git commit -m "Release version ${NEW_VERSION}

${RELEASE_NOTES}"
    echo -e "${GREEN}✓ Changes committed${NC}"
else
    echo -e "${YELLOW}⚠️  No changes to commit${NC}"
fi

# Create git tag
echo -e "\n${BLUE}🏷️  Creating git tag...${NC}"
git tag -a "v${NEW_VERSION}" -m "Release ${NEW_VERSION}

${RELEASE_NOTES}"
echo -e "${GREEN}✓ Tag v${NEW_VERSION} created${NC}"

# Push to GitHub
echo -e "\n${BLUE}📤 Pushing to GitHub...${NC}"
read -p "Push to GitHub? (y/N): " PUSH_CONFIRM

if [[ "$PUSH_CONFIRM" =~ ^[Yy]$ ]]; then
    git push origin master
    git push origin "v${NEW_VERSION}"
    echo -e "${GREEN}✓ Pushed to GitHub${NC}"
else
    echo -e "${YELLOW}⚠️  Skipped GitHub push${NC}"
    echo -e "  To push later, run:"
    echo -e "    git push origin master"
    echo -e "    git push origin v${NEW_VERSION}"
fi

# Publish to PyPI
echo -e "\n${BLUE}📦 Publish to PyPI?${NC}"
read -p "Publish to PyPI? (y/N): " PUBLISH_CONFIRM

if [[ "$PUBLISH_CONFIRM" =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}🚀 Publishing to PyPI...${NC}"
    
    # Check for API token
    if [ -z "$TWINE_API_TOKEN" ] && [ -z "$TWINE_PASSWORD" ]; then
        echo -e "${YELLOW}⚠️  API token not found. Loading from setup script...${NC}"
        if [ -f "scripts/setup-pypi-env.sh" ]; then
            source scripts/setup-pypi-env.sh
        else
            echo -e "${RED}❌ setup-pypi-env.sh not found${NC}"
            echo -e "  Set TWINE_API_TOKEN environment variable or run:"
            echo -e "    source scripts/setup-pypi-env.sh"
            exit 1
        fi
    fi
    
    ./scripts/build-and-publish.sh --publish
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Published to PyPI${NC}"
    else
        echo -e "${RED}❌ PyPI publish failed${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  Skipped PyPI publish${NC}"
    echo -e "  To publish later, run:"
    echo -e "    ./scripts/build-and-publish.sh --publish"
fi

echo -e "\n${GREEN}✅ Release ${NEW_VERSION} complete!${NC}\n"
echo -e "${BLUE}Summary:${NC}"
echo -e "  Version: ${GREEN}${NEW_VERSION}${NC}"
echo -e "  Tag: ${GREEN}v${NEW_VERSION}${NC}"
echo -e "  GitHub: ${GREEN}https://github.com/Vegeta-Bles/dbinit/releases/tag/v${NEW_VERSION}${NC}"
echo -e "  PyPI: ${GREEN}https://pypi.org/project/dbinit/${NEW_VERSION}/${NC}\n"
