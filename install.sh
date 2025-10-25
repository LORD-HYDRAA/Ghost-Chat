#!/bin/sh

echo "🔧 Ghost Chat - Automated Setup"
echo "================================"


if [ "$(uname)" != "Linux" ]; then
    echo "❌ Error: Ghost Chat only runs on Linux systems."
    exit 1
fi

echo "🔄 Checking system dependencies..."


check_package() {
    if ! dpkg -l | grep -q "^ii  $1 "; then
        echo "📦 Installing $1..."
        sudo apt-get install -y "$1"
    else
        echo "✅ $1 already installed"
    fi
}


sudo apt-get update -qq


check_package "python3"
check_package "python3-pip"
check_package "python3-venv"
check_package "tor"
check_package "net-tools"

echo "🔧 Configuring Tor..."

sudo mkdir -p /var/run/tor/
sudo chown debian-tor:debian-tor /var/run/tor/ 2>/dev/null || true
sudo chmod 755 /var/run/tor/ 2>/dev/null || true


echo "🚀 Starting Tor service..."
sudo systemctl enable tor 2>/dev/null || true
sudo systemctl start tor 2>/dev/null || true
sleep 2

echo "🐍 Setting up Python environment..."


if [ ! -d "ghost_env" ]; then
    python3 -m venv ghost_env
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi


. ghost_env/bin/activate

echo "📚 Installing Python packages..."


pip install --upgrade pip
pip install pynacl cryptography stem pysocks

echo "📁 Creating directories..."
mkdir -p src
mkdir -p logs

echo "🔒 Setting permissions..."
chmod +x run.sh 2>/dev/null || true

echo ""
echo "✅ Setup complete! Ghost Chat is ready to use."
echo ""
echo "Quick Start:"
echo "  source ghost_env/bin/activate"
echo "  sudo -E ./run.sh -host -key 'key1' -inner 'key2' -chat 'key3' -username 'Alice'"
echo ""


#  © 2025 LordHydra. All Rights Reserved.
# Proprietary & Confidential. Do not copy, share, or modify.
