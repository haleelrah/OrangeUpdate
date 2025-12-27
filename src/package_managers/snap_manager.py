"""
Snap Package Manager Handler
"""
from typing import List, Dict, Optional
import re
from .base import PackageManager


class SnapManager(PackageManager):
    """Handler for Snap package manager"""
    
    def __init__(self):
        super().__init__()
        self.name = "Snap"
        self.command = "snap"
        self.available = self.check_availability()
    
    def check_availability(self) -> bool:
        """Check if Snap is installed"""
        return self.is_command_available("snap")
    
    def update(self) -> tuple[int, str, str]:
        """Update snap store information"""
        return self.execute_command(["snap", "refresh", "--list"], use_sudo=False)
    
    def upgrade(self, package: Optional[str] = None) -> tuple[int, str, str]:
        """Upgrade packages"""
        if package:
            return self.execute_command(["snap", "refresh", package], use_sudo=False)
        else:
            return self.execute_command(["snap", "refresh"], use_sudo=False)
    
    def search(self, query: str) -> List[Dict[str, str]]:
        """Search for packages"""
        returncode, stdout, stderr = self.execute_command(
            ["snap", "find", query], use_sudo=False
        )
        
        packages = []
        if returncode == 0:
            lines = stdout.split('\n')[1:]  # Skip header
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        packages.append({
                            'name': parts[0],
                            'version': parts[1],
                            'description': ' '.join(parts[3:]) if len(parts) > 3 else '',
                            'manager': 'Snap'
                        })
        return packages
    
    def install(self, package: str) -> tuple[int, str, str]:
        """Install a package"""
        return self.execute_command(["snap", "install", package], use_sudo=False)
    
    def remove(self, package: str) -> tuple[int, str, str]:
        """Remove a package"""
        return self.execute_command(["snap", "remove", package], use_sudo=False)
    
    def list_installed(self) -> List[Dict[str, str]]:
        """List all installed packages"""
        returncode, stdout, stderr = self.execute_command(
            ["snap", "list"], use_sudo=False
        )
        
        packages = []
        if returncode == 0:
            lines = stdout.split('\n')[1:]  # Skip header
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        packages.append({
                            'name': parts[0],
                            'version': parts[1],
                            'description': parts[2] if len(parts) > 2 else '',
                            'manager': 'Snap'
                        })
        return packages
    
    def list_upgradable(self) -> List[Dict[str, str]]:
        """List packages that can be upgraded"""
        returncode, stdout, stderr = self.execute_command(
            ["snap", "refresh", "--list"], use_sudo=False
        )
        
        packages = []
        if returncode == 0:
            lines = stdout.split('\n')[1:]  # Skip header
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        packages.append({
                            'name': parts[0],
                            'current_version': parts[1],
                            'new_version': parts[2],
                            'manager': 'Snap'
                        })
        return packages
