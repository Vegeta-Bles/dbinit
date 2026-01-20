#!/bin/bash
# dbinit Setup Script
# This script can be sourced in your shell profile to run setup on terminal open

# Check if dbinit is installed
if ! command -v dbinit &> /dev/null; then
    echo "dbinit is not installed. Install it with: pip install dbinit"
    return 2>/dev/null || exit 1
fi

# Check if configuration exists
if [ ! -f ~/.dbinit/config.json ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Welcome to dbinit!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "It looks like this is your first time using dbinit."
    echo "Let's set it up!"
    echo ""
    
    if command -v dbinit &> /dev/null; then
        dbinit setup
    else
        echo "Error: dbinit command not found"
        return 2>/dev/null || exit 1
    fi
fi
