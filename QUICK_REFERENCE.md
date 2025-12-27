# 🍊 Orange Update - Quick Reference

## What is Orange Update?

A **universal GUI package manager** for Linux that automatically detects and manages packages from multiple package managers (APT, DNF, Pacman, Flatpak, Snap) without needing terminal commands.

## Project Files

```
OrangeUpdate/
├── orange-update.py        # Main entry point - run this!
├── test_detection.py        # Test which package managers are detected
├── install.sh              # System-wide installation script
├── uninstall.sh            # Removal script
├── requirements.txt        # Python dependencies (PyQt5)
├── README.md               # Full documentation
├── USER_GUIDE.md           # Detailed usage guide
├── LICENSE                 # MIT License
├── .gitignore             # Git ignore file
├── resources/              # Icons and assets (currently empty)
└── src/
    ├── package_managers/   # Backend package manager handlers
    │   ├── base.py        # Abstract base class
    │   ├── apt_manager.py      # Debian/Ubuntu
    │   ├── dnf_manager.py      # Fedora/RHEL
    │   ├── pacman_manager.py   # Arch Linux
    │   ├── flatpak_manager.py  # Universal (Flatpak)
    │   ├── snap_manager.py     # Universal (Snap)
    │   └── detector.py    # Auto-detection system
    └── gui/
        └── main_window.py # PyQt5 GUI application
```

## Quick Start Commands

```bash
# Test detection
python3 test_detection.py

# Run the GUI
python3 orange-update.py

# Install system-wide (optional)
sudo ./install.sh

# Uninstall
sudo ./uninstall.sh
```

## Features at a Glance

✅ **Multi-Package Manager**
- Automatically detects APT, DNF, Pacman, Flatpak, Snap
- Switch between managers with dropdown

✅ **Package Operations**
- View installed packages
- Check for updates
- Search and install new packages
- Remove unwanted packages
- Upgrade individual or all packages

✅ **User-Friendly**
- Clean tabbed interface
- No terminal commands needed
- Real-time operation feedback
- Confirmation dialogs for safety

✅ **Secure**
- Uses pkexec for authentication
- GUI password prompts
- No credential storage

## Supported Distributions

| Distribution | Package Managers |
|--------------|-----------------|
| **Fedora** | DNF + Flatpak + Snap |
| **Ubuntu** | APT + Flatpak + Snap |
| **Debian** | APT + Flatpak |
| **Arch Linux** | Pacman + Flatpak |
| **Manjaro** | Pacman + Flatpak + Snap |
| **openSUSE** | (Add Zypper support) |
| **Any Linux** | Flatpak + Snap |

## Architecture

```
┌─────────────────────────────────────┐
│   GUI (PyQt5 - main_window.py)     │
│  - Main Window                      │
│  - Tabs (Installed/Updates/Search)  │
│  - Worker Threads                   │
└──────────────┬──────────────────────┘
               │
               ↓
┌──────────────────────────────────────┐
│  Detector (detector.py)              │
│  - Scans system                      │
│  - Initializes available managers    │
└──────────────┬───────────────────────┘
               │
               ↓
┌──────────────────────────────────────┐
│  Package Managers (base.py + impls)  │
│  - Abstract interface                │
│  - Individual implementations        │
│  - Execute commands with pkexec      │
└──────────────┬───────────────────────┘
               │
               ↓
┌──────────────────────────────────────┐
│  System (Package Managers)           │
│  - apt, dnf, pacman, flatpak, snap   │
└──────────────────────────────────────┘
```

## Key Classes

### PackageManager (base.py)
Abstract base class defining interface:
- `update()` - Refresh package lists
- `upgrade()` - Upgrade packages
- `search()` - Search for packages
- `install()` - Install package
- `remove()` - Remove package
- `list_installed()` - List installed packages
- `list_upgradable()` - List available updates

### XxxManager classes
Concrete implementations for each package manager.

### PackageManagerDetector
Scans system and initializes available package managers.

### OrangeUpdateGUI
Main PyQt5 application with tabbed interface.

### PackageWorker
QThread for running operations without freezing GUI.

## Dependencies

**Required:**
- Python 3.6+
- PyQt5
- pkexec (usually pre-installed)

**Package Managers (at least one):**
- apt (Debian/Ubuntu)
- dnf (Fedora/RHEL)
- pacman (Arch)
- flatpak (Universal)
- snap (Universal)

## Installation Methods

### Method 1: Run Directly
```bash
cd OrangeUpdate
python3 orange-update.py
```

### Method 2: System Install
```bash
sudo ./install.sh
# Then run from menu or: orange-update
```

### Method 3: Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 orange-update.py
```

## Common Issues

**"No package managers found"**
→ Install at least one supported package manager

**"ModuleNotFoundError: PyQt5"**
→ Install PyQt5: `sudo dnf install python3-pyqt5` (Fedora)
→ Or: `pip3 install PyQt5`

**Authentication fails**
→ Ensure pkexec is installed and PolicyKit is configured

**GUI doesn't start**
→ Check you're in X11/Wayland session
→ Verify PyQt5: `python3 -c "from PyQt5 import QtWidgets"`

## Development

### Adding a New Package Manager

1. Create `src/package_managers/newpm_manager.py`
2. Extend `PackageManager` class
3. Implement all abstract methods
4. Add to `detector.py`:
   ```python
   from .newpm_manager import NewPMManager
   # In detect_managers():
   manager_classes.append(NewPMManager)
   ```

### Testing Changes

```bash
# Test detection
python3 test_detection.py

# Run with debug output
python3 orange-update.py 2>&1 | tee debug.log

# Test specific manager
python3 -c "from src.package_managers.apt_manager import AptManager; m = AptManager(); print(m.list_installed())"
```

## Future Enhancements

- [ ] Package rollback/downgrade support
- [ ] Batch operations (select multiple packages)
- [ ] Advanced filtering and sorting
- [ ] Package details view
- [ ] Update history/log
- [ ] Scheduled automatic updates
- [ ] System tray integration
- [ ] Zypper support (openSUSE)
- [ ] AppImage integration
- [ ] Custom package sources
- [ ] Backup before operations

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Commit: `git commit -m "Add feature"`
5. Push: `git push origin feature-name`
6. Create Pull Request

## License

MIT License - Free to use, modify, and distribute.

## Contact

Part of The Orange Project 🍊
Created: December 27, 2025

---

**Remember:** Always test on a non-production system first!
