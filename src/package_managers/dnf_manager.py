"""
DNF Package Manager Handler (Fedora, RHEL 8+, etc.)
"""
from typing import List, Dict, Optional
import re
from .base import PackageManager


class DnfManager(PackageManager):
    """Handler for DNF package manager"""
    
    def __init__(self):
        super().__init__()
        self.name = "DNF"
        self.command = "dnf"
        self.available = self.check_availability()
    
    def check_availability(self) -> bool:
        """Check if DNF is installed"""
        return self.is_command_available("dnf")
    
    def update(self) -> tuple[int, str, str]:
        """Update package lists"""
        return self.execute_command(["dnf", "check-update"])
    
    def upgrade(self, package: Optional[str] = None) -> tuple[int, str, str]:
        """Upgrade packages"""
        if package:
            return self.execute_command(["dnf", "upgrade", "-y", package])
        else:
            return self.execute_command(["dnf", "upgrade", "-y"])
    
    def search(self, query: str) -> List[Dict[str, str]]:
        """Search for packages"""
        returncode, stdout, stderr = self.execute_command(
            ["dnf", "search", query], use_sudo=False
        )
        
        packages = []
        if returncode == 0:
            lines = stdout.split('\n')
            current_package = None
            for line in lines:
                if line and not line.startswith('=') and not line.startswith('Last metadata'):
                    if ':' in line and not line.startswith(' '):
                        match = re.match(r'^([^\s:]+)\s*:\s*(.+)$', line)
                        if match:
                            current_package = {
                                'name': match.group(1).split('.')[0],
                                'description': match.group(2),
                                'manager': 'DNF'
                            }
                            packages.append(current_package)
        return packages
    
    def install(self, package: str) -> tuple[int, str, str]:
        """Install a package"""
        return self.execute_command(["dnf", "install", "-y", package])
    
    def remove(self, package: str) -> tuple[int, str, str]:
        """Remove a package"""
        return self.execute_command(["dnf", "remove", "-y", package])
    
    def list_installed(self) -> List[Dict[str, str]]:
        """List all installed packages"""
        returncode, stdout, stderr = self.execute_command(
            ["dnf", "list", "installed"], use_sudo=False
        )
        
        packages = []
        if returncode == 0:
            lines = stdout.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('Installed') and not line.startswith('Last metadata'):
                    parts = line.split()
                    if len(parts) >= 2:
                        packages.append({
                            'name': parts[0].split('.')[0],
                            'version': parts[1],
                            'manager': 'DNF'
                        })
        return packages
    
    def list_upgradable(self) -> List[Dict[str, str]]:
        """List packages that can be upgraded"""
        returncode, stdout, stderr = self.execute_command(
            ["dnf", "list", "updates"], use_sudo=False
        )
        
        packages = []
        if returncode == 0:
            lines = stdout.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('Available') and not line.startswith('Last metadata'):
                    parts = line.split()
                    if len(parts) >= 2:
                        packages.append({
                            'name': parts[0].split('.')[0],
                            'new_version': parts[1],
                            'manager': 'DNF'
                        })
        return packages
