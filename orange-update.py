#!/usr/bin/env python3
"""
Orange Update - Universal Package Manager GUI
Entry point for the application
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui.main_window import main

if __name__ == "__main__":
    main()
