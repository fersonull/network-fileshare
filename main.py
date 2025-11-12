#!/usr/bin/env python3
"""
Educational Network File Sharing - Main Entry Point
FOR EDUCATIONAL PURPOSES ONLY

This script provides a simple interface to launch the file sharing tools.
"""

import sys
import os

def show_menu():
    """Display the main menu"""
    print("🌐 Educational Network File Sharing")
    print("=" * 40)
    print("FOR EDUCATIONAL PURPOSES ONLY")
    print("=" * 40)
    print("\nChoose an option:")
    print("1. 🚀 Run Interactive Demo")
    print("2. 📂 Start File Server (share files)")
    print("3. 💻 Start File Client (connect to server)")
    print("4. 🔍 Auto-discover servers")
    print("5. ⚙️  Setup/Install dependencies")
    print("6. 📖 Quick Start Guide")
    print("7. ❌ Exit")
    print("\n⚠️  Remember: Use only on trusted local networks!")

def run_demo():
    """Run the interactive demo"""
    os.system(f"{sys.executable} demo.py")

def start_server():
    """Start the file server"""
    print("\n📂 Starting File Server")
    print("Tips:")
    print("- Add --upload to allow file uploads")
    print("- Add --port XXXX to use a different port")
    print("- Add --directory PATH to share a specific folder")
    
    cmd = input("\nEnter server command (or press Enter for default): ").strip()
    if not cmd:
        cmd = f"{sys.executable} file_server.py --upload"
    else:
        cmd = f"{sys.executable} file_server.py {cmd}"
    
    print(f"Running: {cmd}")
    os.system(cmd)

def start_client():
    """Start the file client"""
    print("\n💻 Starting File Client")
    server_ip = input("Enter server IP address (or press Enter to discover): ").strip()
    
    if not server_ip:
        cmd = f"{sys.executable} file_client.py --discover"
    else:
        cmd = f"{sys.executable} file_client.py {server_ip}"
    
    print(f"Running: {cmd}")
    os.system(cmd)

def discover_servers():
    """Discover available servers"""
    print("\n🔍 Discovering servers on local network...")
    os.system(f"{sys.executable} file_client.py --discover")

def setup():
    """Run setup"""
    print("\n⚙️ Installing dependencies...")
    os.system(f"{sys.executable} setup.py")

def show_guide():
    """Show quick start guide"""
    os.system(f"{sys.executable} demo.py --guide")

def main():
    """Main menu loop"""
    while True:
        try:
            show_menu()
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                run_demo()
            elif choice == "2":
                start_server()
            elif choice == "3":
                start_client()
            elif choice == "4":
                discover_servers()
            elif choice == "5":
                setup()
            elif choice == "6":
                show_guide()
            elif choice == "7":
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-7.")
            
            if choice != "7":
                input("\nPress Enter to return to menu...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except EOFError:
            print("\n\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()