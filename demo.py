#!/usr/bin/env python3
"""
Demo script for Educational Network File Sharing
Creates sample files and demonstrates the file sharing functionality
"""

import os
import tempfile
import subprocess
import sys
import time
import threading
from pathlib import Path

def create_demo_files():
    """Create sample files for demonstration"""
    demo_dir = Path("demo_files")
    demo_dir.mkdir(exist_ok=True)
    
    # Create various types of demo files
    files_to_create = {
        "welcome.txt": "Welcome to the Educational File Sharing Demo!\n\nThis is a sample text file to demonstrate file sharing capabilities.",
        "info.md": "# Demo Information\n\nThis is a **Markdown** file showing how different file types are handled.\n\n- Text files\n- Documents\n- Images (if you add them)\n- Any file type!",
        "data.json": '{\n  "demo": true,\n  "purpose": "educational",\n  "features": [\n    "file browsing",\n    "downloading",\n    "uploading"\n  ]\n}',
        "script_example.py": "#!/usr/bin/env python3\n# This is a demo Python script\n\nprint('Hello from shared file!')\nprint('This demonstrates code file sharing')\n",
        "notes.txt": "Demo Notes:\n\n1. This folder contains sample files\n2. Try downloading them to test the system\n3. Upload your own files to test upload functionality\n4. Navigate between folders to test directory browsing\n\nFor educational purposes only!"
    }
    
    # Create subdirectory with more files
    subdir = demo_dir / "subdirectory"
    subdir.mkdir(exist_ok=True)
    
    subdir_files = {
        "nested_file.txt": "This file is in a subdirectory.\nIt demonstrates directory navigation capabilities.",
        "config.ini": "[Settings]\nmode=demo\neducational=true\nsafe=yes\n\n[Network]\nlocal_only=true\ntrusted_networks_only=true"
    }
    
    print("📁 Creating demo files...")
    
    # Create main demo files
    for filename, content in files_to_create.items():
        file_path = demo_dir / filename
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ Created: {file_path}")
    
    # Create subdirectory files
    for filename, content in subdir_files.items():
        file_path = subdir / filename
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ Created: {file_path}")
    
    return demo_dir

def get_local_ip():
    """Get local IP address"""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        local_ip = sock.getsockname()[0]
        sock.close()
        return local_ip
    except:
        return "127.0.0.1"

def run_demo_server(demo_dir, port=8000):
    """Run the demo server in a separate process"""
    try:
        cmd = [sys.executable, "file_server.py", 
               "--directory", str(demo_dir), 
               "--port", str(port),
               "--upload"]
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except Exception as e:
        print(f"❌ Failed to start demo server: {e}")
        return None

def demo_client_operations(server_ip, port=8000):
    """Demonstrate client operations"""
    try:
        # Import the client class
        sys.path.append('.')
        from file_client import NetworkFileClient
        
        print(f"\n🔗 Connecting to demo server at {server_ip}:{port}")
        client = NetworkFileClient(server_ip, port, "demo_downloads")
        
        if not client.test_connection():
            print("❌ Could not connect to demo server")
            return False
        
        print("✅ Connected successfully!")
        
        # List root directory
        print("\n📂 Listing root directory:")
        directories, files = client.list_directory("/")
        for d in directories:
            print(f"📁 {d['name']}/")
        for f in files:
            print(f"📄 {f['name']}")
        
        # Download a demo file
        if files:
            demo_file = files[0]
            print(f"\n⬇️ Downloading demo file: {demo_file['name']}")
            success = client.download_file(demo_file['path'])
            if success:
                print("✅ Demo download completed")
        
        # List subdirectory if it exists
        if directories:
            subdir = directories[0]
            print(f"\n📂 Listing subdirectory: {subdir['name']}")
            sub_dirs, sub_files = client.list_directory(subdir['path'])
            for f in sub_files:
                print(f"📄 {f['name']}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Could not import client: {e}")
        print("💡 Make sure to install dependencies: python setup.py")
        return False
    except Exception as e:
        print(f"❌ Demo client error: {e}")
        return False

def interactive_demo():
    """Run an interactive demonstration"""
    print("🎓 Educational Network File Sharing Demo")
    print("=" * 50)
    
    # Check dependencies
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("❌ Missing dependencies. Running setup...")
        subprocess.call([sys.executable, "setup.py"])
        print("✅ Setup complete. Please run the demo again.")
        return
    
    print("This demo will:")
    print("1. Create sample files for testing")
    print("2. Start a file server")
    print("3. Demonstrate client operations")
    print("4. Show you how to access via web browser")
    print("\n⚠️ FOR EDUCATIONAL PURPOSES ONLY")
    
    input("\nPress Enter to continue...")
    
    # Create demo files
    demo_dir = create_demo_files()
    print(f"📁 Demo files created in: {demo_dir.absolute()}")
    
    # Get local IP
    local_ip = get_local_ip()
    port = 8001  # Use different port to avoid conflicts
    
    # Start demo server
    print(f"\n🚀 Starting demo server...")
    server_process = run_demo_server(demo_dir, port)
    
    if not server_process:
        print("❌ Failed to start demo server")
        return
    
    # Wait a moment for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    print(f"\n🌐 Demo server is running!")
    print(f"📱 Web access: http://localhost:{port}")
    print(f"🌍 Network access: http://{local_ip}:{port}")
    print(f"📁 Serving directory: {demo_dir.absolute()}")
    
    # Demonstrate client operations
    print(f"\n🔧 Demonstrating client operations...")
    success = demo_client_operations(local_ip, port)
    
    if success:
        print("\n✅ Demo client operations completed successfully!")
    
    print(f"\n🌐 The server is still running. You can:")
    print(f"1. Open your web browser and go to: http://localhost:{port}")
    print(f"2. From another device on the same network, go to: http://{local_ip}:{port}")
    print(f"3. Use the client: python file_client.py {local_ip} --port {port}")
    print(f"4. Test auto-discovery: python file_client.py --discover")
    
    try:
        input("\nPress Enter to stop the demo server and clean up...")
    except KeyboardInterrupt:
        pass
    
    # Clean up
    print("\n🧹 Cleaning up...")
    try:
        server_process.terminate()
        server_process.wait(timeout=5)
    except:
        try:
            server_process.kill()
        except:
            pass
    
    print("✅ Demo completed!")
    print(f"\nDemo files are still available in: {demo_dir.absolute()}")
    print("You can delete this directory when you're done testing.")

def quick_start_guide():
    """Display a quick start guide"""
    print("🚀 Quick Start Guide")
    print("=" * 30)
    print("\n1️⃣ SETUP:")
    print("   python setup.py")
    print("\n2️⃣ START SERVER (on device sharing files):")
    print("   python file_server.py --upload")
    print("\n3️⃣ CONNECT CLIENT (from other device):")
    print("   python file_client.py <server_ip>")
    print("   OR")
    print("   python file_client.py --discover")
    print("\n4️⃣ WEB ACCESS:")
    print("   Open browser: http://<server_ip>:8000")
    print("\n💡 TIP: Run this demo first!")
    print("   python demo.py")

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--guide":
            quick_start_guide()
            return
        elif sys.argv[1] == "--create-files":
            demo_dir = create_demo_files()
            print(f"✅ Demo files created in: {demo_dir.absolute()}")
            return
    
    # Run interactive demo by default
    interactive_demo()

if __name__ == "__main__":
    main()