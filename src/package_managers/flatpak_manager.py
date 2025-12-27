"""
Flatpak Package Manager Handler
"""
from typing import List, Dict, Optional
import re
from .base import PackageManager


class FlatpakManager(PackageManager):
    """Handler for Flatpak package manager"""
    
    def __init__(self):
        super().__init__()
        self.name = "Flatpak"
        self.command = "flatpak"
        self.available = self.check_availability()
    
    def check_availability(self) -> bool:
        """Check if Flatpak is installed"""
        return self.is_command_available("flatpak")
    
    def update(self) -> tuple[int, str, str]:
        """Update Flatpak repositories"""
        return self.execute_command(["flatpak", "update", "--appstream"], use_sudo=False)
    
    def upgrade(self, package: Optional[str] = None) -> tuple[int, str, str]:
        """Upgrade packages"""
        if package:
            return self.execute_command(["flatpak", "update", "-y", package], use_sudo=False)
        else:
            return self.execute_command(["flatpak", "update", "-y"], use_sudo=False)
    
    def search(self, query: str) -> List[Dict[str, str]]:
        """Search for packages"""
        returncode, stdout, stderr = self.execute_command(
            ["flatpak", "search", query], use_sudo=False
        )
        
        packages = []
        if returncode == 0:
            lines = stdout.split('\n')[1:]  # Skip header
            for line in lines:
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) >= 3:
                        packages.append({
                            'name': parts[0].strip(),
                            'description': parts[1].strip(),
                            'app_id': parts[2].strip(),
                            'manager': 'Flatpak'
                        })
        return packages
    
    def install(self, package: str) -> tuple[int, str, str]:
        """Install a package"""
        return self.execute_command(["flatpak", "install", "-y", package], use_sudo=False)
    
    def remove(self, package: str) -> tuple[int, str, str]:
        """Remove a package"""
        return self.execute_command(["flatpak", "uninstall", "-y", package], use_sudo=False)
    
    def list_installed(self) -> List[Dict[str, str]]:
        """List all installed packages"""
        returncode, stdout, stderr = self.execute_command(
            ["flatpak", "list", "--app"], use_sudo=False
        )
        
        packages = []
        if returncode == 0:
            lines = stdout.split('\n')
            for line in lines:
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) >= 3:
                        packages.append({
                            'name': parts[0].strip(),
                            'app_id': parts[1].strip(),
                            'version': parts[2].strip() if len(parts) > 2 else 'N/A',
                            'manager': 'Flatpak'
                        })
        return packages
    
    def list_upgradable(self) -> List[Dict[str, str]]:
        """List packages that can be upgraded"""
        returncode, stdout, stderr = self.execute_command(
            ["flatpak", "remote-ls", "--updates"], use_sudo=False
        )
        
        packages = []
        if returncode == 0:
            lines = stdout.split('\n')
            for line in lines:
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        packages.append({
                            'name': parts[0].strip(),
                            'app_id': parts[1].strip(),
                            'manager': 'Flatpak'
                        })
        return packages
