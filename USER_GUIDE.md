# Orange Update User Guide

## Quick Start

### Running for the First Time

1. **Install dependencies**:
   ```bash
   # Make sure you have Python 3 and PyQt5
   pip3 install -r requirements.txt
   # OR use your system package manager (recommended)
   sudo apt install python3-pyqt5  # Debian/Ubuntu
   ```

2. **Test package manager detection**:
   ```bash
   python3 test_detection.py
   ```
   This will show which package managers are detected on your system.

3. **Launch the GUI**:
   ```bash
   python3 orange-update.py
   ```

### System Installation

For permanent installation with menu integration:

```bash
sudo ./install.sh
```

Then launch from your application menu or run `orange-update` from terminal.

## Interface Overview

### Main Window Components

1. **Package Manager Selector** (top)
   - Drop-down menu to switch between detected package managers
   - Refresh button to reload package lists

2. **Tabs** (center)
   - **Installed Packages**: Browse all installed packages
   - **Available Updates**: See packages with available updates
   - **Search Packages**: Find and install new packages

3. **Action Buttons** (bottom of tabs)
   - **Update Package Lists**: Refresh repository information
   - **Upgrade All Packages**: Install all available updates

4. **Output Panel** (bottom)
   - Shows command output and status messages
   - Helpful for troubleshooting

## Common Tasks

### Updating Your System

1. Click **"Update Package Lists"** to refresh
2. Switch to **"Available Updates"** tab
3. Either:
   - Click **"Upgrade All Packages"** for full system update
   - Click individual **"Upgrade"** buttons for specific packages

### Installing New Software

1. Go to **"Search Packages"** tab
2. Type package name (e.g., "firefox", "gimp", "vlc")
3. Click **"Search"**
4. Click **"Install"** next to desired package
5. Confirm the installation

### Removing Software

1. Go to **"Installed Packages"** tab
2. Find the package you want to remove
3. Click **"Remove"** button
4. Confirm the removal

### Switching Package Managers

If you have multiple package managers (e.g., APT + Flatpak):

1. Use the drop-down at the top to select manager
2. The interface updates to show packages from that manager
3. Each package manager is independent

## Package Manager Specifics

### APT (Debian/Ubuntu)
- Updates system packages
- Requires sudo/pkexec for most operations
- Package names match official Ubuntu/Debian repositories

### DNF (Fedora)
- Modern package manager for Fedora
- Handles dependencies automatically
- Requires sudo/pkexec

### Pacman (Arch Linux)
- Arch's package manager
- Use `--noconfirm` flag automatically
- Requires sudo/pkexec

### Flatpak
- Universal packages that work on any distro
- Does NOT require root privileges
- Apps are sandboxed for security
- Search includes Flathub by default

### Snap
- Ubuntu's universal package format
- Works on many distributions
- Does NOT require root privileges
- Auto-updates in background

## Authentication

Orange Update uses **pkexec** for authentication, which provides:
- GUI password prompt (no terminal needed)
- Secure privilege elevation
- Works with PolicyKit

When you perform operations requiring root:
1. A password dialog appears
2. Enter your user password
3. Operation proceeds with elevated privileges

## Tips & Tricks

### Performance
- Update package lists periodically (weekly is good)
- Flatpak/Snap operations are usually faster than system packages
- Large upgrades may take time - be patient

### Safety
- Always review what will be installed/removed
- System packages (APT/DNF/Pacman) affect core system
- Flatpak/Snap are safer to experiment with

### Troubleshooting
- Check output panel for error messages
- Run `test_detection.py` to verify package managers
- Try running individual commands in terminal to debug
- Some operations may fail if system is already running updates

### Multiple Package Managers
- You can have both system packages AND Flatpak/Snap
- Some apps available in multiple formats - choose based on preference
- Flatpak/Snap are more isolated but may be larger

## Keyboard Shortcuts

- **Ctrl+R**: Refresh packages (when refresh button has focus)
- **Ctrl+F**: Focus search box (in Search tab)
- **Enter**: Execute search (in search box)
- **Tab**: Navigate between fields
- **Ctrl+Q**: Quit application

## Command Line Usage

After installation, you can:

```bash
# Launch GUI
orange-update

# Test detection without GUI
cd /opt/orange-update
python3 test_detection.py

# Run without installation
cd /path/to/OrangeUpdate
python3 orange-update.py
```

## Advanced Features

### Managing Flatpak Remotes

To add Flathub (if not already added):
```bash
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

### Viewing Detailed Package Info

For more details about a package, use terminal:
```bash
apt show package-name        # APT
dnf info package-name        # DNF
pacman -Si package-name      # Pacman
flatpak info app.id          # Flatpak
snap info package-name       # Snap
```

## Known Limitations

- No package rollback yet (coming in future version)
- Cannot manage multiple packages at once (one at a time)
- No advanced filtering or sorting
- Some package managers may show limited descriptions
- Terminal output truncated to prevent UI lag

## Getting Help

If something doesn't work:

1. Check the output panel for error messages
2. Run `test_detection.py` to verify setup
3. Check that package managers are up to date
4. Try the operation manually in terminal to see full error
5. Check file permissions and PolicyKit configuration

## Configuration Files

Orange Update doesn't create config files, but uses:
- System package manager configs (unchanged)
- PolicyKit for authentication
- Standard Python paths for imports

No user data is stored or collected.
