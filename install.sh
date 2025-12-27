#!/bin/bash
# Installation script for Orange Update

set -e

echo "🍊 Orange Update Installer"
echo "=========================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Installation directory
INSTALL_DIR="/opt/orange-update"
DESKTOP_FILE="/usr/share/applications/orange-update.desktop"
BIN_LINK="/usr/local/bin/orange-update"

echo "Installing Orange Update..."

# Create installation directory
mkdir -p "$INSTALL_DIR"

# Copy files
echo "Copying files to $INSTALL_DIR..."
cp -r src "$INSTALL_DIR/"
cp orange-update.py "$INSTALL_DIR/"
cp README.md "$INSTALL_DIR/"

# Make executable
chmod +x "$INSTALL_DIR/orange-update.py"

# Create symlink
echo "Creating symlink..."
ln -sf "$INSTALL_DIR/orange-update.py" "$BIN_LINK"

# Create desktop entry
echo "Creating desktop entry..."
cat > "$DESKTOP_FILE" << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Orange Update
Comment=Universal Package Manager GUI
Exec=pkexec /opt/orange-update/orange-update.py
Icon=system-software-update
Terminal=false
Categories=System;Settings;PackageManager;
Keywords=package;update;upgrade;install;software;apt;dnf;pacman;flatpak;snap;
StartupNotify=true
EOF

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "You can now:"
echo "  1. Launch from your application menu (search for 'Orange Update')"
echo "  2. Run from terminal: orange-update"
echo "  3. Run directly: $INSTALL_DIR/orange-update.py"
echo ""
echo "To uninstall, run: sudo ./uninstall.sh"
