"""
Base class for package managers
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import subprocess
import shutil


class PackageManager(ABC):
    """Abstract base class for all package managers"""
    
    def __init__(self):
        self.name = ""
        self.command = ""
        self.available = False
        
    @abstractmethod
    def check_availability(self) -> bool:
        """Check if this package manager is installed"""
        pass
    
    @abstractmethod
    def update(self) -> tuple[int, str, str]:
        """Update package lists/repositories"""
        pass
    
    @abstractmethod
    def upgrade(self, package: Optional[str] = None) -> tuple[int, str, str]:
        """Upgrade packages"""
        pass
    
    @abstractmethod
    def search(self, query: str) -> List[Dict[str, str]]:
        """Search for packages"""
        pass
    
    @abstractmethod
    def install(self, package: str) -> tuple[int, str, str]:
        """Install a package"""
        pass
    
    @abstractmethod
    def remove(self, package: str) -> tuple[int, str, str]:
        """Remove a package"""
        pass
    
    @abstractmethod
    def list_installed(self) -> List[Dict[str, str]]:
        """List all installed packages"""
        pass
    
    @abstractmethod
    def list_upgradable(self) -> List[Dict[str, str]]:
        """List packages that can be upgraded"""
        pass
    
    def execute_command(self, command: List[str], use_sudo: bool = True) -> tuple[int, str, str]:
        """
        Execute a shell command
        Returns: (return_code, stdout, stderr)
        """
        try:
            if use_sudo and command[0] not in ['flatpak', 'snap']:
                # Use pkexec for GUI authentication
                command = ['pkexec'] + command
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)
    
    def is_command_available(self, command: str) -> bool:
        """Check if a command is available in PATH"""
        return shutil.which(command) is not None
