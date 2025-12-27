#!/bin/bash
# Uninstallation script for Orange Update

set -e

echo "🍊 Orange Update Uninstaller"
echo "============================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Installation paths
INSTALL_DIR="/opt/orange-update"
DESKTOP_FILE="/usr/share/applications/orange-update.desktop"
BIN_LINK="/usr/local/bin/orange-update"

echo "Removing Orange Update..."

# Remove files
if [ -d "$INSTALL_DIR" ]; then
    echo "Removing installation directory..."
    rm -rf "$INSTALL_DIR"
fi

if [ -f "$DESKTOP_FILE" ]; then
    echo "Removing desktop entry..."
    rm -f "$DESKTOP_FILE"
fi

if [ -L "$BIN_LINK" ]; then
    echo "Removing symlink..."
    rm -f "$BIN_LINK"
fi

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications
fi

echo ""
echo "✅ Orange Update has been uninstalled"
