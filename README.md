# Orange Update - Universal Package Manager GUI

A graphical interface to manage packages from multiple package managers on Linux systems.

## Features

- 🔍 **Multi-Package Manager Support**: Automatically detects and manages:
  - APT (Debian, Ubuntu, Mint)
  - DNF (Fedora, RHEL 8+)
  - Pacman (Arch Linux, Manjaro)
  - Flatpak
  - Snap

- 📦 **Package Management**:
  - View installed packages
  - Check for available updates
  - Search for new packages
  - Install and remove packages
  - Upgrade individual or all packages
  
- 🎨 **User-Friendly GUI**:
  - Clean and intuitive interface
  - Tabbed interface for different operations
  - Real-time operation feedback
  - No terminal commands needed

## Installation

### Prerequisites

```bash
# Install Python 3 and PyQt5
# For Debian/Ubuntu:
sudo apt install python3 python3-pyqt5

# For Fedora:
sudo dnf install python3 python3-qt5

# For Arch Linux:
sudo pacman -S python python-pyqt5

# You also need pkexec for authentication:
# Usually pre-installed, but if needed:
sudo apt install policykit-1  # Debian/Ubuntu
sudo dnf install polkit       # Fedora
sudo pacman -S polkit         # Arch
```

### Running Orange Update

1. Clone or download this repository
2. Navigate to the directory:
   ```bash
   cd OrangeUpdate
   ```
3. Make the script executable:
   ```bash
   chmod +x orange-update.py
   ```
4. Run the application:
   ```bash
   python3 orange-update.py
   ```

### System Integration (Optional)

To add Orange Update to your application menu:

```bash
sudo ./install.sh
```

This will:
- Install the application to `/opt/orange-update`
- Create a desktop launcher
- Add it to your system menu

## Usage

1. **Launch** the application
2. **Select** your package manager from the dropdown (if multiple are detected)
3. **Navigate** through tabs:
   - **Installed Packages**: View and remove installed packages
   - **Available Updates**: See and install available updates
   - **Search Packages**: Search and install new packages
4. **Perform Actions**:
   - Click "Update Package Lists" to refresh repository information
   - Click "Upgrade All Packages" to update everything
   - Use individual package buttons for specific operations

## Security

- Orange Update uses `pkexec` for privilege escalation, which provides GUI password prompts
- Flatpak and Snap operations don't require root privileges
- All operations show confirmation dialogs before execution

## Supported Package Managers

| Package Manager | Distributions | Status |
|----------------|---------------|--------|
| APT | Debian, Ubuntu, Mint, Pop!_OS | ✅ Full Support |
| DNF | Fedora, RHEL 8+, CentOS Stream | ✅ Full Support |
| Pacman | Arch Linux, Manjaro, EndeavourOS | ✅ Full Support |
| Flatpak | Universal (all distros) | ✅ Full Support |
| Snap | Ubuntu, many others | ✅ Full Support |

## Development

### Project Structure

```
OrangeUpdate/
├── src/
│   ├── package_managers/
│   │   ├── base.py              # Base package manager class
│   │   ├── apt_manager.py       # APT implementation
│   │   ├── dnf_manager.py       # DNF implementation
│   │   ├── pacman_manager.py    # Pacman implementation
│   │   ├── flatpak_manager.py   # Flatpak implementation
│   │   ├── snap_manager.py      # Snap implementation
│   │   └── detector.py          # System detection
│   └── gui/
│       └── main_window.py       # Main GUI application
├── resources/                    # Icons and assets
├── orange-update.py             # Entry point
└── README.md
```

### Adding New Package Managers

1. Create a new file in `src/package_managers/`
2. Extend the `PackageManager` base class
3. Implement all required methods
4. Add to `detector.py`

## Troubleshooting

### "No package managers found"
- Ensure at least one supported package manager is installed
- Check that package manager commands are in PATH

### Authentication issues
- Make sure `pkexec` is installed
- Check PolicyKit configuration
- Try running with sudo for testing: `sudo python3 orange-update.py`

### GUI doesn't start
- Verify PyQt5 is installed: `python3 -c "from PyQt5 import QtWidgets"`
- Check Python version: Python 3.6+ required

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - Feel free to use and modify as needed.

## Author

Created for The Orange Project 🍊

## Changelog

### Version 1.0.0 (2025-12-27)
- Initial release
- Support for APT, DNF, Pacman, Flatpak, and Snap
- GUI with package listing, updates, and search
- Multi-threaded operations
- pkexec authentication
