"""
Pacman Package Manager Handler (Arch Linux, Manjaro, etc.)
"""
from typing import List, Dict, Optional
import re
from .base import PackageManager


class PacmanManager(PackageManager):
    """Handler for Pacman package manager"""
    
    def __init__(self):
        super().__init__()
        self.name = "Pacman"
        self.command = "pacman"
        self.available = self.check_availability()
    
    def check_availability(self) -> bool:
        """Check if Pacman is installed"""
        return self.is_command_available("pacman")
    
    def update(self) -> tuple[int, str, str]:
        """Update package database"""
        return self.execute_command(["pacman", "-Sy"])
    
    def upgrade(self, package: Optional[str] = None) -> tuple[int, str, str]:
        """Upgrade packages"""
        if package:
            return self.execute_command(["pacman", "-S", "--noconfirm", package])
        else:
            return self.execute_command(["pacman", "-Syu", "--noconfirm"])
    
    def search(self, query: str) -> List[Dict[str, str]]:
        """Search for packages"""
        returncode, stdout, stderr = self.execute_command(
            ["pacman", "-Ss", query], use_sudo=False
        )
        
        packages = []
        if returncode == 0:
            lines = stdout.split('\n')
            i = 0
            while i < len(lines):
                line = lines[i]
                if line.strip() and not line.startswith(' '):
                    match = re.match(r'^([^/]+)/([^\s]+)\s+([^\s]+)', line)
                    if match:
                        description = ""
                        if i + 1 < len(lines) and lines[i + 1].startswith('    '):
                            description = lines[i + 1].strip()
                        packages.append({
                            'name': match.group(2),
                            'version': match.group(3),
                            'description': description,
                            'manager': 'Pacman'
                        })
                i += 1
        return packages
    
    def install(self, package: str) -> tuple[int, str, str]:
        """Install a package"""
        return self.execute_command(["pacman", "-S", "--noconfirm", package])
    
    def remove(self, package: str) -> tuple[int, str, str]:
        """Remove a package"""
        return self.execute_command(["pacman", "-R", "--noconfirm", package])
    
    def list_installed(self) -> List[Dict[str, str]]:
        """List all installed packages"""
        returncode, stdout, stderr = self.execute_command(
            ["pacman", "-Q"], use_sudo=False
        )
        
        packages = []
        if returncode == 0:
            lines = stdout.split('\n')
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        packages.append({
                            'name': parts[0],
                            'version': parts[1],
                            'manager': 'Pacman'
                        })
        return packages
    
    def list_upgradable(self) -> List[Dict[str, str]]:
        """List packages that can be upgraded"""
        returncode, stdout, stderr = self.execute_command(
            ["pacman", "-Qu"], use_sudo=False
        )
        
        packages = []
        if returncode == 0:
            lines = stdout.split('\n')
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 4:
                        packages.append({
                            'name': parts[0],
                            'current_version': parts[1],
                            'new_version': parts[3],
                            'manager': 'Pacman'
                        })
        return packages
