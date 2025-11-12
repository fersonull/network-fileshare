# Network File Sharing

A simple Python-based file sharing system for educational purposes that allows you to share files between devices on the same local network.

## ⚠️ IMPORTANT DISCLAIMER

**This tool is for EDUCATIONAL PURPOSES ONLY.** It should only be used in trusted, local networks for learning about network programming and file sharing concepts. Do not use this in production environments or expose it to the internet.

## 🚀 Quick Start

### 1. Setup
```bash
# Install dependencies
python setup.py
```

### 2. Start File Server (on the device sharing files)
```bash
# Basic server (read-only access)
python file_server.py

# Server with upload capability
python file_server.py --upload

# Server on specific port and directory
python file_server.py --port 9000 --directory /path/to/share --upload
```

### 3. Connect from Client Device
```bash
# Connect to a specific server
python file_client.py 192.168.1.100

# Auto-discover servers on the network
python file_client.py --discover

# Connect with custom port
python file_client.py 192.168.1.100 --port 9000
```

## 📋 Features

### File Server (`file_server.py`)
- **Web-based interface** - Access files through any web browser
- **Directory browsing** - Navigate through folder structure
- **File downloads** - Download files directly
- **File uploads** - Upload files to the server (when enabled)
- **Responsive design** - Works on mobile devices
- **Multi-threaded** - Handles multiple connections simultaneously
- **Security info** - Shows server details and timestamps

### File Client (`file_client.py`)
- **Interactive CLI** - Command-line interface for file operations
- **Auto-discovery** - Find file servers on local network
- **Download management** - Progress tracking for downloads
- **Directory navigation** - Browse remote directories
- **File uploads** - Upload files to remote server
- **Connection testing** - Verify server availability

## 🛠️ Usage Examples

### Starting a File Server

```bash
# Share current directory on default port 8000
python file_server.py

# Share specific directory with uploads enabled
python file_server.py --directory ~/Documents --upload --port 8080

# Share with specific network interface
python file_server.py --host 192.168.1.50 --port 8000
```

**Server will display:**
```
🌐 Educational Network File Server Started
📁 Serving directory: /home/user/Documents
🖥️  Host: 0.0.0.0
🔌 Port: 8000
📤 Upload enabled: True

📱 Access URLs:
   Local: http://localhost:8000
   Network: http://192.168.1.50:8000
```

### Using the File Client

```bash
# Connect to server
python file_client.py 192.168.1.50

# Interactive session
192.168.1.50:/> ls                    # List files
192.168.1.50:/> cd Documents          # Change directory
192.168.1.50:/Documents> download file.txt  # Download file
192.168.1.50:/Documents> upload photo.jpg   # Upload file
192.168.1.50:/Documents> pwd          # Show current path
192.168.1.50:/Documents> quit         # Exit
```

### Auto-Discovery

```bash
python file_client.py --discover

# Output:
🔍 Scanning for file servers on port 8000...
✅ Found file server at 192.168.1.50:8000
✅ Found file server at 192.168.1.75:8000

🎯 Found 2 file server(s):
  1. 192.168.1.50:8000
  2. 192.168.1.75:8000
```

## 🌐 Web Interface

When you start the file server, you can also access it through any web browser:

1. **On the same device**: Visit `http://localhost:8000`
2. **From other devices**: Visit `http://[server-ip]:8000`

The web interface provides:
- 📁 Visual directory listing
- ⬇️ One-click file downloads
- ⬆️ Drag-and-drop file uploads (if enabled)
- 📱 Mobile-friendly responsive design
- 🔙 Easy navigation with breadcrumbs

## 📱 Mobile Access Example

To access files from your mobile phone:

1. **On your computer** (sharing files):
   ```bash
   python file_server.py --upload --directory ~/Pictures
   ```

2. **On your mobile phone**:
   - Connect to the same WiFi network
   - Open web browser
   - Go to: `http://[computer-ip]:8000`
   - Browse and download/upload files

3. **Find your computer's IP**:
   ```bash
   # The server will display the IP when it starts, or use:
   
   # Windows
   ipconfig
   
   # Mac/Linux
   ifconfig
   ip addr show
   ```

## ⚙️ Command Line Options

### File Server Options
```bash
python file_server.py [OPTIONS]

Options:
  --port, -p PORT        Port to listen on (default: 8000)
  --directory, -d DIR    Directory to serve (default: current)
  --upload, -u           Allow file uploads
  --host HOST           Host to bind to (default: 0.0.0.0)
  --help                Show help message
```

### File Client Options
```bash
python file_client.py [SERVER_IP] [OPTIONS]

Arguments:
  SERVER_IP             IP address of the file server

Options:
  --port, -p PORT       Server port (default: 8000)
  --download-dir, -d DIR Download directory (default: downloads)
  --discover, -s        Scan for servers on network
  --help               Show help message
```

## 🔧 Client Commands

When using the interactive client, these commands are available:

| Command | Description | Example |
|---------|-------------|---------|
| `ls` | List files and directories | `ls` |
| `cd <dir>` | Change directory | `cd Documents` |
| `cd ..` | Go to parent directory | `cd ..` |
| `cd /` | Go to root directory | `cd /` |
| `pwd` | Show current directory | `pwd` |
| `download <file>` | Download a file | `download photo.jpg` |
| `upload <file>` | Upload a local file | `upload document.pdf` |
| `help` | Show available commands | `help` |
| `quit` / `exit` | Exit the client | `quit` |

## 🚨 Security Considerations

**IMPORTANT**: This tool is designed for educational purposes only. Here are important security considerations:

### ✅ Safe Usage
- Use only on trusted local networks (home WiFi, etc.)
- Only share files you're comfortable sharing
- Use for learning network programming concepts
- Test file sharing between your own devices

### ❌ Unsafe Usage
- **Never** expose to the internet
- **Never** use on public/untrusted networks
- **Never** share sensitive personal information
- **Never** use in production environments

### 🛡️ Built-in Safety Features
- Only binds to local network by default
- No authentication system (intentionally simple)
- Clear warning messages about educational use
- Local network discovery only

## 🐛 Troubleshooting

### Connection Issues
```bash
# Problem: "Connection failed"
# Solutions:
1. Check if server is running
2. Verify IP address is correct
3. Ensure both devices are on same network
4. Check firewall settings
5. Try different port number
```

### Permission Issues
```bash
# Problem: "Permission denied" on port < 1024
# Solution: Use port >= 1024 or run with elevated privileges
python file_server.py --port 8080
```

### File Access Issues
```bash
# Problem: Cannot access certain directories
# Solution: Check file permissions and run from accessible directory
cd ~/Documents
python file_server.py
```

### Network Discovery Issues
```bash
# Problem: Auto-discovery finds no servers
# Solutions:
1. Ensure server is running
2. Check firewall allows the port
3. Verify same network subnet
4. Try manual IP connection first
```

## 🔍 Network Discovery Details

The auto-discovery feature works by:

1. Determining your local IP address
2. Scanning the entire /24 subnet (e.g., 192.168.1.1-254)
3. Testing each IP for an open port
4. Verifying it's actually a file server
5. Displaying found servers

This is safe because it only scans your local network.

## 📁 File Organization

```
network-file-sharing/
├── file_server.py      # Main server script
├── file_client.py      # Client connection script
├── setup.py           # Dependency installer
├── README.md          # This documentation
└── downloads/         # Default download directory (created automatically)
```

## 🎓 Educational Value

This project demonstrates several important concepts:

- **Network Programming**: TCP/IP, HTTP protocol, client-server architecture
- **Web Development**: HTML generation, HTTP request handling, form processing
- **File I/O**: Reading, writing, and transferring files
- **Threading**: Handling multiple concurrent connections
- **Security**: Understanding network security implications
- **User Interface**: Both web and command-line interfaces

## 🤝 Contributing

This is an educational project. Feel free to:
- Add features for learning purposes
- Improve the user interface
- Add better error handling
- Enhance security features for educational understanding

Remember to keep the focus on educational value and safety.

## 📜 License

This project is for educational purposes only. Use responsibly and only in appropriate environments.

---

**Happy Learning! 🎓**

Remember: Always prioritize security and use this tool responsibly in safe, controlled environments for educational exploration of network file sharing concepts.