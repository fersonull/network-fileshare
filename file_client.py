#!/usr/bin/env python3
"""
Educational Network File Client
This script connects to a file server and allows browsing and downloading files
over a local network. FOR EDUCATIONAL PURPOSES ONLY.

Usage:
    python file_client.py <server_ip> [--port PORT] [--download-dir DIRECTORY]
"""

import requests
import os
import sys
import argparse
import urllib.parse
from bs4 import BeautifulSoup
import re
from pathlib import Path

class NetworkFileClient:
    def __init__(self, server_ip, port=8000, download_dir="downloads"):
        self.server_ip = server_ip
        self.port = port
        self.base_url = f"http://{server_ip}:{port}"
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.timeout = 30
    
    def test_connection(self):
        """Test if the server is reachable"""
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            print(f"✅ Successfully connected to {self.base_url}")
            return True
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection failed: Cannot reach {self.base_url}")
            return False
        except requests.exceptions.Timeout:
            print(f"❌ Connection timeout: Server at {self.base_url} is not responding")
            return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def list_directory(self, path="/"):
        """List files and directories at the given path"""
        try:
            url = urllib.parse.urljoin(self.base_url, path)
            response = self.session.get(url)
            response.raise_for_status()
            
            # Parse HTML to extract file links
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', class_='file-name')
            
            files = []
            directories = []
            
            for link in links:
                href = link.get('href')
                name = link.get_text().strip()
                
                if href and not href.startswith('http'):  # Local links only
                    if name.endswith('/'):
                        directories.append({
                            'name': name[:-1],  # Remove trailing slash
                            'path': urllib.parse.urljoin(path, href),
                            'type': 'directory'
                        })
                    else:
                        files.append({
                            'name': name,
                            'path': urllib.parse.urljoin(path, href),
                            'type': 'file'
                        })
            
            return directories, files
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error listing directory: {e}")
            return [], []
    
    def download_file(self, remote_path, local_name=None):
        """Download a file from the server"""
        try:
            url = urllib.parse.urljoin(self.base_url, remote_path)
            
            if local_name is None:
                local_name = os.path.basename(remote_path) or "downloaded_file"
            
            local_path = self.download_dir / local_name
            
            print(f"📥 Downloading: {remote_path}")
            print(f"   Saving to: {local_path}")
            
            response = self.session.get(url, stream=True)
            response.raise_for_status()
            
            # Get file size if available
            total_size = int(response.headers.get('content-length', 0))
            
            with open(local_path, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r   Progress: {progress:.1f}% ({downloaded}/{total_size} bytes)", end='')
                        else:
                            print(f"\r   Downloaded: {downloaded} bytes", end='')
            
            print(f"\n✅ Download completed: {local_path}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Download failed: {e}")
            return False
        except IOError as e:
            print(f"❌ File write error: {e}")
            return False
    
    def upload_file(self, local_file_path, remote_path="/"):
        """Upload a file to the server"""
        try:
            local_path = Path(local_file_path)
            if not local_path.exists():
                print(f"❌ Local file not found: {local_path}")
                return False
            
            url = urllib.parse.urljoin(self.base_url, remote_path)
            
            print(f"📤 Uploading: {local_path}")
            print(f"   To server path: {remote_path}")
            
            with open(local_path, 'rb') as f:
                files = {'file': (local_path.name, f, 'application/octet-stream')}
                response = self.session.post(url, files=files)
                response.raise_for_status()
            
            print(f"✅ Upload completed")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Upload failed: {e}")
            return False
        except IOError as e:
            print(f"❌ File read error: {e}")
            return False

def interactive_mode(client):
    """Interactive file browser mode"""
    current_path = "/"
    
    print("\n🌐 Interactive File Browser")
    print("Commands: ls, cd <dir>, download <file>, upload <local_file>, pwd, help, quit")
    print("=" * 60)
    
    while True:
        try:
            command = input(f"{client.server_ip}:{current_path}> ").strip()
            
            if not command:
                continue
            
            parts = command.split()
            cmd = parts[0].lower()
            
            if cmd == 'quit' or cmd == 'exit':
                print("👋 Goodbye!")
                break
            
            elif cmd == 'help':
                print("\nAvailable commands:")
                print("  ls                    - List files and directories")
                print("  cd <directory>        - Change directory")
                print("  download <file>       - Download a file")
                print("  upload <local_file>   - Upload a file")
                print("  pwd                   - Show current directory")
                print("  help                  - Show this help")
                print("  quit/exit             - Exit the program")
            
            elif cmd == 'pwd':
                print(f"Current path: {current_path}")
            
            elif cmd == 'ls':
                directories, files = client.list_directory(current_path)
                
                if not directories and not files:
                    print("📁 Directory is empty or inaccessible")
                    continue
                
                print(f"\n📁 Directory listing for: {current_path}")
                print("-" * 50)
                
                # Show directories first
                for d in directories:
                    print(f"📁 {d['name']}/")
                
                # Then show files
                for f in files:
                    print(f"📄 {f['name']}")
                print()
            
            elif cmd == 'cd':
                if len(parts) < 2:
                    print("❌ Usage: cd <directory>")
                    continue
                
                target = parts[1]
                
                if target == "..":
                    # Go to parent directory
                    if current_path != "/":
                        current_path = "/".join(current_path.rstrip("/").split("/")[:-1]) or "/"
                elif target == "/":
                    current_path = "/"
                else:
                    # Check if target directory exists
                    directories, _ = client.list_directory(current_path)
                    dir_exists = any(d['name'] == target for d in directories)
                    
                    if dir_exists:
                        if current_path == "/":
                            current_path = f"/{target}"
                        else:
                            current_path = f"{current_path.rstrip('/')}/{target}"
                    else:
                        print(f"❌ Directory not found: {target}")
            
            elif cmd == 'download':
                if len(parts) < 2:
                    print("❌ Usage: download <filename>")
                    continue
                
                filename = parts[1]
                file_path = f"{current_path.rstrip('/')}/{filename}"
                client.download_file(file_path)
            
            elif cmd == 'upload':
                if len(parts) < 2:
                    print("❌ Usage: upload <local_filename>")
                    continue
                
                local_file = parts[1]
                client.upload_file(local_file, current_path)
            
            else:
                print(f"❌ Unknown command: {cmd}. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break

def discover_servers(port=8000, timeout=2):
    """Discover file servers on the local network"""
    import socket
    import threading
    import ipaddress
    
    print(f"🔍 Scanning for file servers on port {port}...")
    
    # Get local network range
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        local_ip = sock.getsockname()[0]
        sock.close()
        
        # Assume /24 subnet
        network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)
        
    except Exception:
        print("❌ Could not determine local network range")
        return []
    
    found_servers = []
    
    def check_host(ip):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((str(ip), port))
            sock.close()
            
            if result == 0:
                # Verify it's our file server by checking HTTP response
                try:
                    import requests
                    response = requests.get(f"http://{ip}:{port}", timeout=timeout)
                    if "Directory listing" in response.text:
                        found_servers.append(str(ip))
                        print(f"✅ Found file server at {ip}:{port}")
                except:
                    pass
        except:
            pass
    
    # Use threading to speed up scanning
    threads = []
    for ip in network.hosts():
        if str(ip) != local_ip:  # Skip own IP
            thread = threading.Thread(target=check_host, args=(ip,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    return found_servers

def main():
    parser = argparse.ArgumentParser(description='Educational Network File Client')
    parser.add_argument('server_ip', nargs='?', help='IP address of the file server')
    parser.add_argument('--port', '-p', type=int, default=8000,
                       help='Port of the file server (default: 8000)')
    parser.add_argument('--download-dir', '-d', default='downloads',
                       help='Directory to save downloaded files (default: downloads)')
    parser.add_argument('--discover', '-s', action='store_true',
                       help='Scan for file servers on local network')
    
    args = parser.parse_args()
    
    if args.discover:
        servers = discover_servers(args.port)
        if servers:
            print(f"\n🎯 Found {len(servers)} file server(s):")
            for i, server in enumerate(servers, 1):
                print(f"  {i}. {server}:{args.port}")
            print()
        else:
            print("❌ No file servers found on the local network")
        return
    
    if not args.server_ip:
        print("❌ Error: Server IP address is required")
        print("Use --discover to scan for servers or provide an IP address")
        parser.print_help()
        sys.exit(1)
    
    # Create client and test connection
    client = NetworkFileClient(args.server_ip, args.port, args.download_dir)
    
    print("🌐 Educational Network File Client")
    print("=" * 50)
    print(f"📡 Connecting to: {args.server_ip}:{args.port}")
    print(f"📁 Download directory: {args.download_dir}")
    print("⚠️  FOR EDUCATIONAL PURPOSES ONLY")
    print("=" * 50)
    
    if not client.test_connection():
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure the file server is running on the target device")
        print("2. Check that both devices are on the same network")
        print("3. Verify the IP address and port number")
        print("4. Check firewall settings on both devices")
        sys.exit(1)
    
    # Start interactive mode
    interactive_mode(client)

if __name__ == "__main__":
    # Install required dependencies if not present
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError as e:
        print(f"❌ Missing required dependency: {e}")
        print("\n📦 Please install required packages:")
        print("pip install requests beautifulsoup4")
        sys.exit(1)
    
    main()