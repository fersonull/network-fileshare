#!/usr/bin/env python3
"""
Setup script for the Educational Network File Sharing tools
This script installs dependencies and sets up the environment
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required Python packages"""
    required_packages = [
        'requests',
        'beautifulsoup4',
        'cgi'
    ]
    
    print("📦 Installing required dependencies...")
    
    for package in required_packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    return True

def make_executable():
    """Make scripts executable on Unix-like systems"""
    if os.name != 'nt':  # Not Windows
        scripts = ['file_server.py', 'file_client.py']
        for script in scripts:
            try:
                os.chmod(script, 0o755)
                print(f"✅ Made {script} executable")
            except OSError:
                print(f"⚠️  Could not make {script} executable")

def main():
    print("🚀 Educational Network File Sharing Setup")
    print("=" * 50)
    
    # Install dependencies
    if install_dependencies():
        print("✅ All dependencies installed successfully")
    else:
        print("❌ Some dependencies failed to install")
        return False
    
    # Make scripts executable
    make_executable()
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. On the device you want to share files FROM:")
    print("   python file_server.py --upload")
    print("\n2. On the device you want to connect TO the shared files:")
    print("   python file_client.py <server_ip_address>")
    print("\n3. Or discover servers automatically:")
    print("   python file_client.py --discover")
    
    return True

if __name__ == "__main__":
    main()