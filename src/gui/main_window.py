"""
Main GUI for Orange Update - Universal Package Manager
"""
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableWidget, QTableWidgetItem, QPushButton, QLabel,
    QLineEdit, QTextEdit, QMessageBox, QProgressDialog, QHeaderView,
    QComboBox, QSplitter, QGroupBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from package_managers.detector import PackageManagerDetector


class PackageWorker(QThread):
    """Worker thread for package operations to prevent GUI freezing"""
    finished = pyqtSignal(int, str, str)
    progress = pyqtSignal(str)
    
    def __init__(self, manager, operation, *args):
        super().__init__()
        self.manager = manager
        self.operation = operation
        self.args = args
    
    def run(self):
        """Execute the package operation"""
        try:
            if self.operation == "update":
                result = self.manager.update()
            elif self.operation == "upgrade":
                result = self.manager.upgrade(*self.args)
            elif self.operation == "install":
                result = self.manager.install(*self.args)
            elif self.operation == "remove":
                result = self.manager.remove(*self.args)
            elif self.operation == "search":
                packages = self.manager.search(*self.args)
                self.finished.emit(0, str(packages), "")
                return
            elif self.operation == "list_installed":
                packages = self.manager.list_installed()
                self.finished.emit(0, str(packages), "")
                return
            elif self.operation == "list_upgradable":
                packages = self.manager.list_upgradable()
                self.finished.emit(0, str(packages), "")
                return
            else:
                result = (-1, "", "Unknown operation")
            
            self.finished.emit(result[0], result[1], result[2])
        except Exception as e:
            self.finished.emit(-1, "", str(e))


class OrangeUpdateGUI(QMainWindow):
    """Main window for Orange Update"""
    
    def __init__(self):
        super().__init__()
        self.detector = PackageManagerDetector()
        self.current_manager = None
        self.worker = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Orange Update - Universal Package Manager")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title
        title = QLabel("🍊 Orange Update")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Package Manager Selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Package Manager:"))
        
        self.manager_combo = QComboBox()
        managers = self.detector.get_available_managers()
        
        if not managers:
            QMessageBox.warning(
                self, "No Package Managers",
                "No supported package managers found on this system!"
            )
        else:
            for manager in managers:
                self.manager_combo.addItem(manager.name)
            self.current_manager = managers[0]
        
        self.manager_combo.currentIndexChanged.connect(self.on_manager_changed)
        selector_layout.addWidget(self.manager_combo)
        selector_layout.addStretch()
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.refresh_packages)
        selector_layout.addWidget(self.refresh_btn)
        
        main_layout.addLayout(selector_layout)
        
        # Create tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Create tabs
        self.create_installed_tab()
        self.create_updates_tab()
        self.create_search_tab()
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.update_btn = QPushButton("📥 Update Package Lists")
        self.update_btn.clicked.connect(self.update_package_lists)
        button_layout.addWidget(self.update_btn)
        
        self.upgrade_all_btn = QPushButton("⬆️ Upgrade All Packages")
        self.upgrade_all_btn.clicked.connect(self.upgrade_all_packages)
        button_layout.addWidget(self.upgrade_all_btn)
        
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        # Status/Output area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMaximumHeight(150)
        main_layout.addWidget(QLabel("Output:"))
        main_layout.addWidget(self.output_text)
        
        # Initial load
        self.refresh_packages()
    
    def create_installed_tab(self):
        """Create the installed packages tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Table for installed packages
        self.installed_table = QTableWidget()
        self.installed_table.setColumnCount(3)
        self.installed_table.setHorizontalHeaderLabels(["Package Name", "Version", "Actions"])
        self.installed_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.installed_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.installed_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.installed_table)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Installed Packages")
    
    def create_updates_tab(self):
        """Create the updates available tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Table for upgradable packages
        self.updates_table = QTableWidget()
        self.updates_table.setColumnCount(4)
        self.updates_table.setHorizontalHeaderLabels(
            ["Package Name", "Current Version", "New Version", "Actions"]
        )
        self.updates_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.updates_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.updates_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.updates_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.updates_table)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Available Updates")
    
    def create_search_tab(self):
        """Create the search packages tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Search bar
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter package name...")
        self.search_input.returnPressed.connect(self.search_packages)
        search_layout.addWidget(self.search_input)
        
        self.search_btn = QPushButton("🔍 Search")
        self.search_btn.clicked.connect(self.search_packages)
        search_layout.addWidget(self.search_btn)
        
        layout.addLayout(search_layout)
        
        # Search results table
        self.search_table = QTableWidget()
        self.search_table.setColumnCount(3)
        self.search_table.setHorizontalHeaderLabels(["Package Name", "Description", "Actions"])
        self.search_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.search_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.search_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.search_table)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Search Packages")
    
    def on_manager_changed(self, index):
        """Handle package manager selection change"""
        managers = self.detector.get_available_managers()
        if 0 <= index < len(managers):
            self.current_manager = managers[index]
            self.refresh_packages()
    
    def refresh_packages(self):
        """Refresh package lists"""
        if not self.current_manager:
            return
        
        self.log_output(f"Refreshing package lists for {self.current_manager.name}...")
        
        # Load installed packages
        self.load_installed_packages()
        
        # Load upgradable packages
        self.load_upgradable_packages()
    
    def load_installed_packages(self):
        """Load installed packages into table"""
        self.installed_table.setRowCount(0)
        packages = self.current_manager.list_installed()
        
        self.installed_table.setRowCount(len(packages))
        for i, pkg in enumerate(packages):
            self.installed_table.setItem(i, 0, QTableWidgetItem(pkg.get('name', '')))
            self.installed_table.setItem(i, 1, QTableWidgetItem(pkg.get('version', '')))
            
            # Add remove button
            remove_btn = QPushButton("🗑️ Remove")
            remove_btn.clicked.connect(lambda checked, p=pkg['name']: self.remove_package(p))
            self.installed_table.setCellWidget(i, 2, remove_btn)
        
        self.log_output(f"Loaded {len(packages)} installed packages")
    
    def load_upgradable_packages(self):
        """Load upgradable packages into table"""
        self.updates_table.setRowCount(0)
        packages = self.current_manager.list_upgradable()
        
        self.updates_table.setRowCount(len(packages))
        for i, pkg in enumerate(packages):
            self.updates_table.setItem(i, 0, QTableWidgetItem(pkg.get('name', '')))
            self.updates_table.setItem(i, 1, QTableWidgetItem(pkg.get('current_version', 'N/A')))
            self.updates_table.setItem(i, 2, QTableWidgetItem(pkg.get('new_version', 'N/A')))
            
            # Add upgrade button
            upgrade_btn = QPushButton("⬆️ Upgrade")
            upgrade_btn.clicked.connect(lambda checked, p=pkg['name']: self.upgrade_package(p))
            self.updates_table.setCellWidget(i, 3, upgrade_btn)
        
        self.log_output(f"Found {len(packages)} available updates")
    
    def search_packages(self):
        """Search for packages"""
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self, "Empty Search", "Please enter a search term")
            return
        
        self.log_output(f"Searching for '{query}'...")
        self.search_table.setRowCount(0)
        
        packages = self.current_manager.search(query)
        
        self.search_table.setRowCount(len(packages))
        for i, pkg in enumerate(packages):
            self.search_table.setItem(i, 0, QTableWidgetItem(pkg.get('name', '')))
            self.search_table.setItem(i, 1, QTableWidgetItem(pkg.get('description', '')))
            
            # Add install button
            install_btn = QPushButton("📦 Install")
            install_btn.clicked.connect(lambda checked, p=pkg['name']: self.install_package(p))
            self.search_table.setCellWidget(i, 2, install_btn)
        
        self.log_output(f"Found {len(packages)} packages")
    
    def update_package_lists(self):
        """Update package lists/repositories"""
        if not self.current_manager:
            return
        
        reply = QMessageBox.question(
            self, "Update Package Lists",
            f"Update package lists for {self.current_manager.name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.run_operation("update")
    
    def upgrade_all_packages(self):
        """Upgrade all packages"""
        if not self.current_manager:
            return
        
        reply = QMessageBox.question(
            self, "Upgrade All Packages",
            f"Upgrade all packages using {self.current_manager.name}?\nThis may take some time.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.run_operation("upgrade")
    
    def upgrade_package(self, package_name):
        """Upgrade a specific package"""
        reply = QMessageBox.question(
            self, "Upgrade Package",
            f"Upgrade package '{package_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.run_operation("upgrade", package_name)
    
    def install_package(self, package_name):
        """Install a package"""
        reply = QMessageBox.question(
            self, "Install Package",
            f"Install package '{package_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.run_operation("install", package_name)
    
    def remove_package(self, package_name):
        """Remove a package"""
        reply = QMessageBox.question(
            self, "Remove Package",
            f"Remove package '{package_name}'?\nThis action may remove dependencies.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.run_operation("remove", package_name)
    
    def run_operation(self, operation, *args):
        """Run a package operation in a worker thread"""
        self.log_output(f"Running {operation}...")
        
        # Disable buttons during operation
        self.set_buttons_enabled(False)
        
        # Create and start worker thread
        self.worker = PackageWorker(self.current_manager, operation, *args)
        self.worker.finished.connect(self.on_operation_finished)
        self.worker.start()
    
    def on_operation_finished(self, returncode, stdout, stderr):
        """Handle completion of package operation"""
        self.set_buttons_enabled(True)
        
        if returncode == 0:
            self.log_output("✓ Operation completed successfully")
            if stdout:
                self.log_output(stdout[:1000])  # Limit output
            self.refresh_packages()
            QMessageBox.information(self, "Success", "Operation completed successfully!")
        else:
            self.log_output(f"✗ Operation failed (return code: {returncode})")
            if stderr:
                self.log_output(f"Error: {stderr[:1000]}")
            QMessageBox.critical(self, "Error", f"Operation failed:\n{stderr[:500]}")
    
    def set_buttons_enabled(self, enabled):
        """Enable/disable all action buttons"""
        self.update_btn.setEnabled(enabled)
        self.upgrade_all_btn.setEnabled(enabled)
        self.refresh_btn.setEnabled(enabled)
        self.search_btn.setEnabled(enabled)
    
    def log_output(self, text):
        """Add text to output area"""
        self.output_text.append(text)


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    window = OrangeUpdateGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
