# Ghost Chat - Lord Hydra Edition

**The Most Secure, Temporary, Memory-Only Chat System**  
*Temporary • Private • Decentralized • Freedom*

## 🚨 Important Security Notice

> ⚠️ **WARNING**: This tool is for educational and legitimate privacy purposes only. Users are solely responsible for complying with local laws and regulations.

## 📖 Overview

Ghost Chat is an **ultra-secure, ephemeral chat system** that operates entirely in RAM with zero disk writes. It combines military-grade encryption with Tor anonymity and your own custom secret language.

## ✨ Features

- **🔒 Triple-Layer Encryption**: AES-256 + NaCl/Noise + Custom Mapping
- **🌐 Tor Hidden Services**: Ephemeral .onion addresses
- **💾 Memory-Only Operation**: No disk writes, complete wipe on exit
- **⚡ Peer-to-Peer**: No central servers
- **🎭 Custom Language**: Your own word-to-code mappings
- **🚀 Temporary**: Everything vanishes when you exit

## 🚀 Quick Start

### Prerequisites
- Linux system
- Python 3.8+
- Tor service

### Installation & Usage

```bash
# Clone the repository
git clone https://github.com/LORD-HYDRAA/Ghost-Chat
cd ghost-chat

# Host a chat room
sudo -E ./run.sh -host -key "your_outer_key" -inner "your_inner_key" -chat "your_chat_key" -username "YourName"

# Join a chat room
./run.sh -join -key "your_outer_key" -inner "your_inner_key" -chat "your_chat_key" -username "YourName" -address "onion_address.onion"
