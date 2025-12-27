#!/bin/bash
# Development helper script for Orange Update

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

show_help() {
    cat << EOF
🍊 Orange Update - Development Helper

Usage: ./dev.sh [command]

Commands:
    test        Run package manager detection test
    run         Launch the GUI application
    check       Check Python and dependencies
    install     Install system dependencies
    clean       Remove Python cache files
    help        Show this help message

Examples:
    ./dev.sh test      # Test package detection
    ./dev.sh run       # Launch GUI
    ./dev.sh check     # Verify setup
EOF
}

check_dependencies() {
    echo "🔍 Checking dependencies..."
    echo ""
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        echo "✅ Python: $PYTHON_VERSION"
    else
        echo "❌ Python 3 not found"
        exit 1
    fi
    
    # Check PyQt5
    if python3 -c "import PyQt5" 2>/dev/null; then
        echo "✅ PyQt5 is installed"
    else
        echo "❌ PyQt5 not found"
        echo "   Install with: pip3 install PyQt5"
        echo "   Or system package: sudo dnf install python3-pyqt5"
    fi
    
    # Check pkexec
    if command -v pkexec &> /dev/null; then
        echo "✅ pkexec is available"
    else
        echo "❌ pkexec not found (needed for authentication)"
    fi
    
    # Check package managers
    echo ""
    echo "📦 Available package managers:"
    
    command -v apt &> /dev/null && echo "  ✓ APT" || echo "  ✗ APT"
    command -v dnf &> /dev/null && echo "  ✓ DNF" || echo "  ✗ DNF"
    command -v pacman &> /dev/null && echo "  ✓ Pacman" || echo "  ✗ Pacman"
    command -v flatpak &> /dev/null && echo "  ✓ Flatpak" || echo "  ✗ Flatpak"
    command -v snap &> /dev/null && echo "  ✓ Snap" || echo "  ✗ Snap"
}

install_deps() {
    echo "📥 Installing dependencies..."
    echo ""
    
    # Detect distro and install
    if [ -f /etc/fedora-release ]; then
        echo "Detected Fedora/RHEL"
        sudo dnf install -y python3 python3-qt5
    elif [ -f /etc/debian_version ]; then
        echo "Detected Debian/Ubuntu"
        sudo apt update
        sudo apt install -y python3 python3-pyqt5
    elif [ -f /etc/arch-release ]; then
        echo "Detected Arch Linux"
        sudo pacman -S --noconfirm python python-pyqt5
    else
        echo "Unknown distribution. Please install manually:"
        echo "  - Python 3"
        echo "  - PyQt5"
    fi
}

run_test() {
    echo "🧪 Running package manager detection test..."
    echo ""
    python3 test_detection.py
}

run_gui() {
    echo "🚀 Launching Orange Update GUI..."
    echo ""
    python3 orange-update.py
}

clean_cache() {
    echo "🧹 Cleaning Python cache files..."
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
    find . -type f -name "*.pyc" -delete 2>/dev/null
    find . -type f -name "*.pyo" -delete 2>/dev/null
    echo "✅ Cache cleaned"
}

# Main script
case "$1" in
    test)
        run_test
        ;;
    run)
        run_gui
        ;;
    check)
        check_dependencies
        ;;
    install)
        install_deps
        ;;
    clean)
        clean_cache
        ;;
    help|--help|-h|"")
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
