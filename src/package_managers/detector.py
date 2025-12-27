"""
Package Manager Detector - Scans system for available package managers
"""
from typing import List
from .apt_manager import AptManager
from .dnf_manager import DnfManager
from .pacman_manager import PacmanManager
from .flatpak_manager import FlatpakManager
from .snap_manager import SnapManager


class PackageManagerDetector:
    """Detects and initializes available package managers on the system"""
    
    def __init__(self):
        self.managers = []
        self.detect_managers()
    
    def detect_managers(self) -> List:
        """Detect all available package managers"""
        # List of all supported package managers
        manager_classes = [
            AptManager,
            DnfManager,
            PacmanManager,
            FlatpakManager,
            SnapManager
        ]
        
        self.managers = []
        for manager_class in manager_classes:
            try:
                manager = manager_class()
                if manager.available:
                    self.managers.append(manager)
                    print(f"✓ Detected: {manager.name}")
                else:
                    print(f"✗ Not found: {manager.name}")
            except Exception as e:
                print(f"✗ Error checking {manager_class.__name__}: {e}")
        
        return self.managers
    
    def get_available_managers(self) -> List:
        """Get list of available package managers"""
        return self.managers
    
    def get_manager_by_name(self, name: str):
        """Get a specific manager by name"""
        for manager in self.managers:
            if manager.name.lower() == name.lower():
                return manager
        return None
