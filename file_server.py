#!/usr/bin/env python3
"""
Educational Network File Server
This script creates a simple HTTP file server that allows browsing and downloading files
over a local network. FOR EDUCATIONAL PURPOSES ONLY.

Usage:
    python file_server.py [--port PORT] [--directory DIRECTORY] [--upload]
    
Security Note: This is for educational use only. Do not use in production environments.
"""

import http.server
import socketserver
import os
import sys
import argparse
import socket
import urllib.parse
import html
import io
import shutil
from datetime import datetime

class FileServerHandler(http.server.SimpleHTTPRequestHandler):
    """Enhanced file server handler with upload capabilities"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def list_directory(self, path):
        """Enhanced directory listing with better UI"""
        try:
            list_items = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None
        
        list_items.sort(key=lambda a: a.lower())
        
        # Create HTML response
        encoded_path = html.escape(urllib.parse.unquote(self.path), quote=False)
        title = f'Directory listing for {encoded_path}'
        
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            margin: 20px; 
            background-color: #f5f5f5;
        }}
        .container {{ 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .upload-form {{
            background: #e9ecef;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .file-list {{
            list-style: none;
            padding: 0;
        }}
        .file-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            border-bottom: 1px solid #eee;
        }}
        .file-item:hover {{
            background-color: #f8f9fa;
        }}
        .file-name {{
            flex-grow: 1;
            text-decoration: none;
            color: #007bff;
        }}
        .file-name:hover {{
            text-decoration: underline;
        }}
        .file-size {{
            margin-left: 10px;
            color: #666;
            font-size: 0.9em;
        }}
        .directory {{
            font-weight: bold;
        }}
        .back-link {{
            background: #6c757d;
            color: white;
            padding: 8px 16px;
            text-decoration: none;
            border-radius: 4px;
            display: inline-block;
            margin-bottom: 20px;
        }}
        .upload-btn {{
            background: #28a745;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }}
        .info {{
            background: #d1ecf1;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
        </div>
        
        <div class="info">
            <strong>Server Info:</strong> {socket.gethostname()} | 
            <strong>Current Path:</strong> {os.path.abspath(path)} |
            <strong>Time:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </div>
'''
        
        # Add upload form if upload is enabled
        if hasattr(self.server, 'allow_upload') and self.server.allow_upload:
            html_content += '''
        <div class="upload-form">
            <h3>Upload File</h3>
            <form enctype="multipart/form-data" method="post">
                <input type="file" name="file" required>
                <input type="submit" value="Upload" class="upload-btn">
            </form>
        </div>
'''
        
        # Add parent directory link
        if self.path != '/':
            parent = '/'.join(self.path.rstrip('/').split('/')[:-1]) or '/'
            html_content += f'<a href="{parent}" class="back-link">← Parent Directory</a>'
        
        html_content += '<ul class="file-list">'
        
        # List directories and files
        for name in list_items:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
                file_class = "directory"
                size_info = "Directory"
            elif os.path.islink(fullname):
                displayname = name + "@"
                file_class = "symlink"
                size_info = "Symlink"
            else:
                file_class = "file"
                try:
                    size = os.path.getsize(fullname)
                    size_info = self.format_file_size(size)
                except OSError:
                    size_info = "Unknown size"
            
            html_content += f'''
            <li class="file-item">
                <a href="{urllib.parse.quote(linkname, errors='surrogatepass')}" class="file-name {file_class}">
                    {html.escape(displayname, quote=False)}
                </a>
                <span class="file-size">{size_info}</span>
            </li>'''
        
        html_content += '''
        </ul>
    </div>
</body>
</html>'''
        
        # Send response
        encoded = html_content.encode('utf-8', 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f
    
    def format_file_size(self, size):
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
    
    def do_POST(self):
        """Handle file upload"""
        if not (hasattr(self.server, 'allow_upload') and self.server.allow_upload):
            self.send_error(405, "Upload not allowed")
            return
        
        content_type = self.headers.get('Content-Type', '')
        if not content_type.startswith('multipart/form-data'):
            self.send_error(400, "Bad request")
            return
        
        try:
            # Parse the multipart form data using email.message
            from email.message import EmailMessage
            from email import message_from_bytes
            import tempfile
            
            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error(400, "No content")
                return
            
            # Read the entire request body
            post_data = self.rfile.read(content_length)
            
            # Parse multipart data manually (simplified approach)
            boundary = None
            for param in content_type.split(';'):
                param = param.strip()
                if param.startswith('boundary='):
                    boundary = param.split('=', 1)[1].strip('"')
                    break
            
            if not boundary:
                self.send_error(400, "No boundary found")
                return
            
            # Split by boundary
            boundary = boundary.encode()
            parts = post_data.split(b'--' + boundary)
            
            filename = None
            file_data = None
            
            for part in parts:
                if b'Content-Disposition' in part and b'filename=' in part:
                    # Extract filename
                    lines = part.split(b'\r\n')
                    for line in lines:
                        if b'Content-Disposition' in line:
                            line_str = line.decode('utf-8', errors='ignore')
                            if 'filename=' in line_str:
                                # Extract filename from Content-Disposition header
                                import re
                                match = re.search(r'filename[^;=\n]*=(["\']?)([^"\';]*)\1', line_str)
                                if match:
                                    filename = match.group(2)
                                break
                    
                    # Extract file data (after double CRLF)
                    if b'\r\n\r\n' in part:
                        header_end = part.find(b'\r\n\r\n')
                        file_data = part[header_end + 4:]
                        # Remove trailing CRLF if present
                        if file_data.endswith(b'\r\n'):
                            file_data = file_data[:-2]
                    break
            
            if filename and file_data is not None:
                # Save the file
                upload_path = os.path.join(self.translate_path(self.path), filename)
                # Ensure safe filename
                filename = os.path.basename(filename)  # Prevent directory traversal
                upload_path = os.path.join(self.translate_path(self.path), filename)
                
                with open(upload_path, 'wb') as f:
                    f.write(file_data)
                
                # Send success response
                self.send_response(302)
                self.send_header('Location', self.path)
                self.end_headers()
            else:
                self.send_error(400, "No file found in request")
                
        except Exception as e:
            self.send_error(500, f"Upload failed: {str(e)}")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Threaded TCP Server to handle multiple connections"""
    allow_reuse_address = True
    daemon_threads = True

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote address to determine local IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        local_ip = sock.getsockname()[0]
        sock.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def main():
    parser = argparse.ArgumentParser(description='Educational Network File Server')
    parser.add_argument('--port', '-p', type=int, default=8000, 
                       help='Port to listen on (default: 8000)')
    parser.add_argument('--directory', '-d', default='../../../exposed', 
                       help='Directory to serve (default: current directory)')
    parser.add_argument('--upload', '-u', action='store_true',
                       help='Allow file uploads')
    parser.add_argument('--host', default='0.0.0.0',
                       help='Host to bind to (default: 0.0.0.0 for all interfaces)')
    
    args = parser.parse_args()
    
    # Change to the specified directory
    if args.directory != '.':
        try:
            os.chdir(args.directory)
        except OSError as e:
            print(f"Error: Cannot change to directory '{args.directory}': {e}")
            sys.exit(1)
    
    # Create server
    try:
        with ThreadedTCPServer((args.host, args.port), FileServerHandler) as httpd:
            # Add upload capability flag
            httpd.allow_upload = args.upload
            
            local_ip = get_local_ip()
            print("=" * 60)
            print("🌐 Educational Network File Server Started")
            print("=" * 60)
            print(f"📁 Serving directory: {os.path.abspath('.')}")
            print(f"🖥️  Host: {args.host}")
            print(f"🔌 Port: {args.port}")
            print(f"📤 Upload enabled: {args.upload}")
            print("\n📱 Access URLs:")
            print(f"   Local: http://localhost:{args.port}")
            print(f"   Network: http://{local_ip}:{args.port}")
            print("\n⚠️  WARNING: This server is for educational purposes only!")
            print("   Do not use in production or expose to the internet.")
            print("\n🛑 Press Ctrl+C to stop the server")
            print("=" * 60)
            
            httpd.serve_forever()
    except PermissionError:
        print(f"Error: Permission denied. Try using a different port (current: {args.port})")
        print("Ports below 1024 require administrator/root privileges.")
        sys.exit(1)
    except OSError as e:
        print(f"Error starting server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()