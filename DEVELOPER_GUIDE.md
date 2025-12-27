# Developer's Guide to Orange Update

## For Developers Who Want to Understand, Modify, or Extend the Code

### Quick Navigation
- [Code Structure](#code-structure)
- [Key Concepts](#key-concepts)
- [Adding Features](#adding-features)
- [Testing](#testing)
- [Best Practices](#best-practices)

---

## Code Structure

### Entry Point: `orange-update.py`

```python
#!/usr/bin/env python3
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui.main_window import main

if __name__ == "__main__":
    main()
```

Simple! Just imports and calls the GUI's main function.

---

## Key Concepts

### 1. Abstract Base Class Pattern

**File:** `src/package_managers/base.py`

```python
class PackageManager(ABC):
    """All package managers must implement these methods"""
    
    @abstractmethod
    def update(self) -> tuple[int, str, str]:
        """Refresh package lists"""
        pass
    
    @abstractmethod
    def install(self, package: str) -> tuple[int, str, str]:
        """Install a package"""
        pass
    
    # ... more abstract methods
```

**Why?** Ensures all package managers have the same interface.

### 2. Command Execution

**Method:** `execute_command()` in `base.py`

```python
def execute_command(self, command: List[str], use_sudo: bool = True):
    """Execute with automatic privilege escalation"""
    if use_sudo and command[0] not in ['flatpak', 'snap']:
        command = ['pkexec'] + command
    
    result = subprocess.run(command, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr
```

**Key Points:**
- Prepends `pkexec` for commands needing root
- Flatpak/Snap don't need root
- Captures all output
- Returns (returncode, stdout, stderr)

### 3. Package Manager Detection

**File:** `src/package_managers/detector.py`

```python
class PackageManagerDetector:
    def detect_managers(self):
        """Check which package managers are available"""
        manager_classes = [AptManager, DnfManager, ...]
        
        for manager_class in manager_classes:
            manager = manager_class()
            if manager.available:  # check_availability() was called
                self.managers.append(manager)
```

**Flow:**
1. Create instance of each manager
2. Manager's `__init__` calls `check_availability()`
3. `check_availability()` uses `shutil.which()` to find command
4. If available, add to list

### 4. GUI Threading

**File:** `src/gui/main_window.py`

```python
class PackageWorker(QThread):
    """Runs operations in background"""
    finished = pyqtSignal(int, str, str)
    
    def run(self):
        # This runs in a separate thread!
        result = self.manager.install(package)
        self.finished.emit(*result)  # Signal back to main thread

class OrangeUpdateGUI(QMainWindow):
    def install_package(self, package):
        # Create worker
        self.worker = PackageWorker(self.manager, "install", package)
        self.worker.finished.connect(self.on_operation_finished)
        self.worker.start()  # Start background thread
```

**Why Threading?**
- Package operations can take minutes
- GUI would freeze without threading
- QThread allows safe background operations
- Signals/slots communicate between threads

---

## Adding Features

### Add a New Package Manager

**Example: Adding Homebrew support**

1. **Create file:** `src/package_managers/brew_manager.py`

```python
from typing import List, Dict, Optional
from .base import PackageManager

class BrewManager(PackageManager):
    def __init__(self):
        super().__init__()
        self.name = "Homebrew"
        self.command = "brew"
        self.available = self.check_availability()
    
    def check_availability(self) -> bool:
        return self.is_command_available("brew")
    
    def update(self) -> tuple[int, str, str]:
        return self.execute_command(["brew", "update"], use_sudo=False)
    
    def upgrade(self, package: Optional[str] = None) -> tuple[int, str, str]:
        if package:
            return self.execute_command(["brew", "upgrade", package], use_sudo=False)
        return self.execute_command(["brew", "upgrade"], use_sudo=False)
    
    def search(self, query: str) -> List[Dict[str, str]]:
        returncode, stdout, stderr = self.execute_command(
            ["brew", "search", query], use_sudo=False
        )
        
        packages = []
        if returncode == 0:
            for line in stdout.split('\n'):
                if line.strip():
                    packages.append({
                        'name': line.strip(),
                        'description': '',
                        'manager': 'Homebrew'
                    })
        return packages
    
    def install(self, package: str) -> tuple[int, str, str]:
        return self.execute_command(["brew", "install", package], use_sudo=False)
    
    def remove(self, package: str) -> tuple[int, str, str]:
        return self.execute_command(["brew", "uninstall", package], use_sudo=False)
    
    def list_installed(self) -> List[Dict[str, str]]:
        returncode, stdout, stderr = self.execute_command(
            ["brew", "list"], use_sudo=False
        )
        
        packages = []
        if returncode == 0:
            for line in stdout.split('\n'):
                if line.strip():
                    packages.append({
                        'name': line.strip(),
                        'version': 'N/A',
                        'manager': 'Homebrew'
                    })
        return packages
    
    def list_upgradable(self) -> List[Dict[str, str]]:
        returncode, stdout, stderr = self.execute_command(
            ["brew", "outdated"], use_sudo=False
        )
        
        packages = []
        if returncode == 0:
            for line in stdout.split('\n'):
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        packages.append({
                            'name': parts[0],
                            'current_version': parts[1],
                            'new_version': parts[-1] if len(parts) > 2 else 'latest',
                            'manager': 'Homebrew'
                        })
        return packages
```

2. **Register in detector:** Edit `src/package_managers/detector.py`

```python
from .brew_manager import BrewManager  # Add import

class PackageManagerDetector:
    def detect_managers(self):
        manager_classes = [
            AptManager,
            DnfManager,
            PacmanManager,
            FlatpakManager,
            SnapManager,
            BrewManager,  # Add this!
        ]
        # ... rest of method
```

3. **Done!** Orange Update now supports Homebrew.

### Add a GUI Feature

**Example: Add "Select All" button**

Edit `src/gui/main_window.py`:

```python
def create_updates_tab(self):
    # ... existing code ...
    
    # Add button layout
    button_layout = QHBoxLayout()
    
    select_all_btn = QPushButton("Select All")
    select_all_btn.clicked.connect(self.select_all_updates)
    button_layout.addWidget(select_all_btn)
    
    upgrade_selected_btn = QPushButton("Upgrade Selected")
    upgrade_selected_btn.clicked.connect(self.upgrade_selected)
    button_layout.addWidget(upgrade_selected_btn)
    
    layout.addLayout(button_layout)

def select_all_updates(self):
    """Select all checkboxes in updates table"""
    for row in range(self.updates_table.rowCount()):
        checkbox = self.updates_table.cellWidget(row, 0)
        if checkbox:
            checkbox.setChecked(True)

def upgrade_selected(self):
    """Upgrade all selected packages"""
    selected = []
    for row in range(self.updates_table.rowCount()):
        checkbox = self.updates_table.cellWidget(row, 0)
        if checkbox and checkbox.isChecked():
            package = self.updates_table.item(row, 1).text()
            selected.append(package)
    
    if selected:
        for package in selected:
            self.upgrade_package(package)
```

---

## Testing

### Unit Testing a Package Manager

```python
# test_dnf_manager.py
import unittest
from src.package_managers.dnf_manager import DnfManager

class TestDnfManager(unittest.TestCase):
    def setUp(self):
        self.manager = DnfManager()
    
    def test_availability(self):
        # Only runs on systems with DNF
        if self.manager.available:
            self.assertEqual(self.manager.name, "DNF")
            self.assertEqual(self.manager.command, "dnf")
    
    def test_search(self):
        if self.manager.available:
            results = self.manager.search("python")
            self.assertIsInstance(results, list)
            if results:
                self.assertIn('name', results[0])
                self.assertIn('manager', results[0])
                self.assertEqual(results[0]['manager'], 'DNF')

if __name__ == '__main__':
    unittest.main()
```

### Integration Testing

```bash
# Test full workflow
./dev.sh test              # Check detection
python3 orange-update.py   # Launch GUI manually
# Then test each operation through GUI
```

---

## Best Practices

### 1. Error Handling

```python
def list_installed(self) -> List[Dict[str, str]]:
    try:
        returncode, stdout, stderr = self.execute_command(...)
        
        if returncode != 0:
            print(f"Error: {stderr}")
            return []
        
        # Parse output
        packages = []
        # ... parsing logic ...
        return packages
        
    except Exception as e:
        print(f"Exception in list_installed: {e}")
        return []
```

### 2. Parsing Output

```python
# Good: Robust parsing with error checking
for line in stdout.split('\n'):
    if not line.strip():
        continue
    
    match = re.match(r'^(\S+)\s+(\S+)', line)
    if match:
        packages.append({
            'name': match.group(1),
            'version': match.group(2)
        })

# Bad: Assumes output format
parts = line.split()
packages.append({'name': parts[0], 'version': parts[1]})  # May crash!
```

### 3. GUI Updates

```python
# Good: Use signals from worker thread
class PackageWorker(QThread):
    finished = pyqtSignal(int, str, str)
    
    def run(self):
        result = self.manager.install(package)
        self.finished.emit(*result)  # Signal to main thread

# Bad: Update GUI from worker thread
def run(self):
    result = self.manager.install(package)
    self.gui.log_output(result)  # WRONG! Not thread-safe!
```

### 4. Command Construction

```python
# Good: List of arguments
command = ["dnf", "install", "-y", package_name]
self.execute_command(command)

# Bad: String with shell=True (security risk!)
command = f"dnf install -y {package_name}"
subprocess.run(command, shell=True)  # Vulnerable to injection!
```

---

## Debugging

### Enable Verbose Output

```python
# In base.py, add debug flag
class PackageManager(ABC):
    def __init__(self):
        self.debug = True  # Enable debug output
    
    def execute_command(self, command, use_sudo=True):
        if self.debug:
            print(f"Executing: {' '.join(command)}")
        
        result = subprocess.run(...)
        
        if self.debug:
            print(f"Return code: {result.returncode}")
            print(f"Output: {result.stdout[:200]}")
        
        return result.returncode, result.stdout, result.stderr
```

### GUI Debugging

```python
# Add to main_window.py
import traceback

def on_operation_finished(self, returncode, stdout, stderr):
    try:
        # ... existing code ...
    except Exception as e:
        print(f"Error in on_operation_finished: {e}")
        traceback.print_exc()
```

### Run in Terminal to See Output

```bash
python3 orange-update.py 2>&1 | tee debug.log
```

---

## Code Patterns

### Pattern 1: Manager Implementation Template

```python
from .base import PackageManager
from typing import List, Dict, Optional

class NewManager(PackageManager):
    def __init__(self):
        super().__init__()
        self.name = "Name"
        self.command = "command"
        self.available = self.check_availability()
    
    def check_availability(self) -> bool:
        return self.is_command_available(self.command)
    
    def update(self) -> tuple[int, str, str]:
        return self.execute_command([self.command, "update"])
    
    # Implement all abstract methods...
```

### Pattern 2: Output Parsing

```python
def parse_output(self, stdout: str) -> List[Dict]:
    packages = []
    
    for line in stdout.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Use regex for robust parsing
        match = re.match(r'^pattern', line)
        if match:
            packages.append({
                'name': match.group(1),
                'version': match.group(2)
            })
    
    return packages
```

### Pattern 3: GUI Button with Confirmation

```python
def remove_package(self, package_name):
    reply = QMessageBox.question(
        self, "Confirm",
        f"Remove {package_name}?",
        QMessageBox.Yes | QMessageBox.No
    )
    
    if reply == QMessageBox.Yes:
        self.run_operation("remove", package_name)
```

---

## Performance Tips

1. **Cache package lists** - Don't query every time
2. **Limit output** - Truncate long outputs
3. **Use generators** for large lists
4. **Profile with cProfile** for bottlenecks

```python
# Example: Caching
class OrangeUpdateGUI:
    def __init__(self):
        self.package_cache = {}
        self.cache_timeout = 300  # 5 minutes
    
    def get_installed_packages(self):
        now = time.time()
        cache_key = f"{self.current_manager.name}_installed"
        
        if cache_key in self.package_cache:
            cached_time, packages = self.package_cache[cache_key]
            if now - cached_time < self.cache_timeout:
                return packages
        
        # Cache miss - query manager
        packages = self.current_manager.list_installed()
        self.package_cache[cache_key] = (now, packages)
        return packages
```

---

## Contributing

### Code Style

- Use **4 spaces** for indentation
- Follow **PEP 8** style guide
- Add **docstrings** to all functions
- Use **type hints** where possible
- Keep functions **under 50 lines**

### Commit Messages

```
Format: <type>: <description>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- refactor: Code refactoring
- test: Add tests
- style: Formatting

Examples:
feat: Add Homebrew package manager support
fix: Handle empty package lists in APT manager
docs: Update installation instructions
```

### Pull Request Process

1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Update documentation
6. Submit PR with description

---

## Resources

### Python/PyQt5
- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Qt for Python](https://doc.qt.io/qtforpython/)

### Package Managers
- [APT Manual](https://manpages.debian.org/bullseye/apt/apt.8.en.html)
- [DNF Documentation](https://dnf.readthedocs.io/)
- [Pacman Manual](https://archlinux.org/pacman/pacman.8.html)
- [Flatpak Docs](https://docs.flatpak.org/)
- [Snap Documentation](https://snapcraft.io/docs)

---

**Happy coding! 🍊**

If you have questions or need help, refer to:
- `ARCHITECTURE.md` - System design
- `BUILD_SUMMARY.md` - Complete overview
- `QUICK_REFERENCE.md` - Quick lookups
