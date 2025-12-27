#!/usr/bin/env python3
"""
Test script to verify package manager detection
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from package_managers.detector import PackageManagerDetector

print("=" * 60)
print("🍊 Orange Update - Package Manager Detection Test")
print("=" * 60)
print()

detector = PackageManagerDetector()
managers = detector.get_available_managers()

print(f"\n✅ Found {len(managers)} package manager(s) on this system:\n")

for manager in managers:
    print(f"  • {manager.name} ({manager.command})")
    
    # Test listing installed packages (limited)
    try:
        installed = manager.list_installed()
        print(f"    - Installed packages: {len(installed)}")
    except Exception as e:
        print(f"    - Error listing installed: {e}")
    
    # Test listing upgradable packages
    try:
        upgradable = manager.list_upgradable()
        print(f"    - Available updates: {len(upgradable)}")
    except Exception as e:
        print(f"    - Error listing updates: {e}")
    
    print()

if not managers:
    print("❌ No supported package managers found!")
    print("\nSupported package managers:")
    print("  - APT (apt)")
    print("  - DNF (dnf)")
    print("  - Pacman (pacman)")
    print("  - Flatpak (flatpak)")
    print("  - Snap (snap)")

print("=" * 60)
print("\nTo launch the GUI, run: python3 orange-update.py")
print("=" * 60)
