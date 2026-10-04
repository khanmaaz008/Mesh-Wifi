# Mesh Wi-Fi Chat

A lightweight Python desktop chat application that allows two computers to communicate in real time over a local Wi-Fi/LAN network using TCP/IP sockets.

## Features

- 💬 Real-time text messaging
- 🌐 Local Wi-Fi/LAN communication
- 🖥️ Server and client modes
- 🕒 Message timestamps
- 🎨 Dark-themed graphical interface
- 🔌 Connection status monitoring
- 🧵 Background message receiving
- ⚡ Lightweight and easy to use

## Requirements

- Windows 10/11
- Python 3.9+
- Same Wi-Fi/LAN network
- TCP port `5000` available

## Installation

Clone the repository:

```bash
https://github.com/khanmaaz008/Mesh-Wifi.git
cd Mesh-Wifi
```

Install the required package:

```bash
pip install customtkinter
```

## Run

Start the application:

```bash
python Mesh-V2.py
```

## How to Use

### Host Computer

1. Open the application.
2. Click **Create Server**.
3. Wait for the other computer to connect.
4. Start chatting.

### Client Computer

1. Open the application.
2. Enter the host computer's IP address.
3. Click **Connect**.
4. Start chatting.

Both computers must be connected to the same local network.

## Configuration

The default communication port is:

```text
5000
```

The port can be changed in `Mesh-V2.py`:

```python
PORT = 5000
```

## Project Structure

```text
Mesh-Wifi/
│
├── Mesh-V2.py
├── README.md
└── LICENSE
```

## Technology

- Python
- CustomTkinter
- TCP/IP Sockets
- Multithreading
- Tkinter

## Note

Despite the project name, the current version uses direct TCP/IP communication between two computers. It does not currently implement true multi-hop mesh networking.

## License

This project is open source. See the `LICENSE` file for details.
