#!/bin/bash
# Build and publish script for dbinit

set -e  # Exit on error

echo "🔨 Building dbinit package..."

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info dbinit.egg-info

# Build the package
echo "Building package..."
python3 -m build

# Check the build
echo "Checking package..."
python3 -m twine check dist/*

# Show what was built
echo ""
echo "📦 Built packages:"
ls -lh dist/

echo ""
echo "✅ Build complete!"

# Optional: publish if flag is set
if [ "$1" == "--publish" ]; then
    echo ""
    echo "🚀 Publishing to PyPI..."
    
    # Check for API token in environment
    if [ -z "$TWINE_PASSWORD" ]; then
        echo "⚠️  TWINE_PASSWORD not set in environment."
        echo "Setting from TWINE_API_TOKEN if available..."
        
        if [ -n "$TWINE_API_TOKEN" ]; then
            export TWINE_PASSWORD="$TWINE_API_TOKEN"
        else
            echo "❌ Error: No API token found!"
            echo "Set TWINE_API_TOKEN or TWINE_PASSWORD environment variable."
            echo ""
            echo "Example:"
            echo "  export TWINE_API_TOKEN='your-token-here'"
            echo "  ./scripts/build-and-publish.sh --publish"
            exit 1
        fi
    fi
    
    # Set username if not already set
    if [ -z "$TWINE_USERNAME" ]; then
        export TWINE_USERNAME="__token__"
    fi
    
    python3 -m twine upload dist/*
    echo ""
    echo "✅ Published successfully!"
else
    echo ""
    echo "To publish to PyPI, run:"
    echo "  ./scripts/build-and-publish.sh --publish"
    echo ""
    echo "Make sure to set your API token:"
    echo "  export TWINE_API_TOKEN='your-token-here'"
fi
