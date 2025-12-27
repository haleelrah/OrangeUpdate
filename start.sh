#!/bin/bash
# Quick start script for Orange Update

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        🍊 Orange Update - Quick Start Guide 🍊             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Welcome to Orange Update - Universal Package Manager GUI!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 STEP 1: Check Dependencies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
./dev.sh check
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 STEP 2: Install Missing Dependencies (if needed)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if PyQt5 is installed
if ! python3 -c "import PyQt5" 2>/dev/null; then
    echo "⚠️  PyQt5 is not installed!"
    echo ""
    echo "Would you like to install it now? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        if [ -f /etc/fedora-release ]; then
            echo "Installing PyQt5 on Fedora..."
            sudo dnf install -y python3-pyqt5
        elif [ -f /etc/debian_version ]; then
            echo "Installing PyQt5 on Debian/Ubuntu..."
            sudo apt update && sudo apt install -y python3-pyqt5
        elif [ -f /etc/arch-release ]; then
            echo "Installing PyQt5 on Arch..."
            sudo pacman -S --noconfirm python-pyqt5
        else
            echo "Installing PyQt5 via pip..."
            pip3 install PyQt5
        fi
    else
        echo "Skipping installation. You can install later with:"
        echo "  sudo dnf install python3-pyqt5  # Fedora"
        echo "  sudo apt install python3-pyqt5  # Ubuntu"
        echo "  pip3 install PyQt5              # Any distro"
        exit 0
    fi
else
    echo "✅ All dependencies are installed!"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 STEP 3: Test Package Manager Detection"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
python3 test_detection.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Ready to Launch!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Launch Orange Update GUI? (y/n)"
read -r launch
if [[ "$launch" =~ ^[Yy]$ ]]; then
    echo ""
    echo "🎉 Starting Orange Update..."
    python3 orange-update.py
else
    echo ""
    echo "You can launch Orange Update anytime with:"
    echo "  python3 orange-update.py"
    echo ""
    echo "Or install system-wide with:"
    echo "  sudo ./install.sh"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📚 Documentation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  README.md           - Full project documentation"
echo "  USER_GUIDE.md       - Detailed usage instructions"
echo "  QUICK_REFERENCE.md  - Quick command reference"
echo "  PROJECT_STATUS.md   - Current status and features"
echo ""
echo "🍊 Enjoy Orange Update!"
