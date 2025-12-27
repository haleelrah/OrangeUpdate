"""
APT Package Manager Handler (Debian, Ubuntu, etc.)
"""
from typing import List, Dict, Optional
import re
from .base import PackageManager


class AptManager(PackageManager):
    """Handler for APT package manager"""
    
    def __init__(self):
        super().__init__()
        self.name = "APT"
        self.command = "apt"
        self.available = self.check_availability()
    
    def check_availability(self) -> bool:
        """Check if APT is installed"""
        return self.is_command_available("apt")
    
    def update(self) -> tuple[int, str, str]:
        """Update package lists"""
        return self.execute_command(["apt", "update"])
    
    def upgrade(self, package: Optional[str] = None) -> tuple[int, str, str]:
        """Upgrade packages"""
        if package:
            return self.execute_command(["apt", "install", "--only-upgrade", "-y", package])
        else:
            return self.execute_command(["apt", "upgrade", "-y"])
    
    def search(self, query: str) -> List[Dict[str, str]]:
        """Search for packages"""
        returncode, stdout, stderr = self.execute_command(
            ["apt", "search", query], use_sudo=False
        )
        
        packages = []
        if returncode == 0:
            lines = stdout.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('Sorting') and not line.startswith('Full Text'):
                    match = re.match(r'^([^\s/]+).*?-\s+(.+)$', line)
                    if match:
                        packages.append({
                            'name': match.group(1),
                            'description': match.group(2),
                            'manager': 'APT'
                        })
        return packages
    
    def install(self, package: str) -> tuple[int, str, str]:
        """Install a package"""
        return self.execute_command(["apt", "install", "-y", package])
    
    def remove(self, package: str) -> tuple[int, str, str]:
        """Remove a package"""
        return self.execute_command(["apt", "remove", "-y", package])
    
    def list_installed(self) -> List[Dict[str, str]]:
        """List all installed packages"""
        returncode, stdout, stderr = self.execute_command(
            ["dpkg", "-l"], use_sudo=False
        )
        
        packages = []
        if returncode == 0:
            lines = stdout.split('\n')
            for line in lines:
                if line.startswith('ii'):
                    parts = line.split(None, 4)
                    if len(parts) >= 4:
                        packages.append({
                            'name': parts[1],
                            'version': parts[2],
                            'description': parts[4] if len(parts) > 4 else '',
                            'manager': 'APT'
                        })
        return packages
    
    def list_upgradable(self) -> List[Dict[str, str]]:
        """List packages that can be upgraded"""
        returncode, stdout, stderr = self.execute_command(
            ["apt", "list", "--upgradable"], use_sudo=False
        )
        
        packages = []
        if returncode == 0:
            lines = stdout.split('\n')
            for line in lines[1:]:  # Skip header
                if line.strip() and not line.startswith('Listing'):
                    match = re.match(r'^([^\s/]+).*?\s+(\S+)\s+.*?\[upgradable from:\s+(\S+)\]', line)
                    if match:
                        packages.append({
                            'name': match.group(1),
                            'new_version': match.group(2),
                            'current_version': match.group(3),
                            'manager': 'APT'
                        })
        return packages
