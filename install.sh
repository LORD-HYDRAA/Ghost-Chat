echo "🔧 Ghost Chat - Automated Setup"
echo "================================"


if [[ "$(uname)" != "Linux" ]]; then
    echo "❌ Error: Ghost Chat only runs on Linux systems."
    exit 1
fi
# © 2025 LordHydra. All Rights Reserved.
# Proprietary & Confidential. Do not copy, share, or modify.

install_package() {
    local package=$1
    if ! dpkg -l | grep -q "^ii  $package "; then
        echo "📦 Installing $package..."
        sudo apt-get install -y $package
    else
        echo "✅ $package already installed"
    fi
}


echo "🔄 Updating package manager..."
sudo apt-get update -qq


echo "📥 Installing system dependencies..."
install_package "python3"
install_package "python3-pip"
install_package "python3-venv"
install_package "tor"
install_package "net-tools"


echo "🔧 Configuring Tor..."
sudo mkdir -p /var/run/tor/
sudo chown debian-tor:debian-tor /var/run/tor/
sudo chmod 755 /var/run/tor/


TOR_CONFIG="/etc/tor/torrc"
if ! grep -q "ControlPort 9050" "$TOR_CONFIG"; then
    echo "⚙️  Updating Tor configuration..."
    sudo tee -a "$TOR_CONFIG" > /dev/null <<EOF

# Ghost Chat Configuration
ControlPort 9050
CookieAuthentication 1
CookieAuthFileGroupReadable 1
EOF
fi

echo "🚀 Starting Tor service..."
sudo systemctl enable tor
sudo systemctl start tor
sudo systemctl status tor --no-pager -l

echo "🐍 Setting up Python virtual environment..."
if [ ! -d "ghost_env" ]; then
    python3 -m venv ghost_env
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo "📚 Installing Python packages..."
source ghost_env/bin/activate


pip install --upgrade pip


pip install pynacl cryptography stem pysocks


echo "📁 Setting up directories..."
mkdir -p src
mkdir -p logs


echo "🔒 Setting up Tor permissions..."
sudo usermod -a -G debian-tor $USER || true
sudo chmod 755 /var/run/tor/ || true

echo ""
echo "✅ Setup complete! Ghost Chat is ready to use."
echo ""
echo "Quick Start:"
echo "  Host: ./run.sh -host -key 'key1' -inner 'key2' -chat 'key3' -username 'Alice'"
echo "  Join: ./run.sh -join -key 'key1' -inner 'key2' -chat 'key3' -username 'Bob' -address 'onion_address'"
echo ""

#  © 2025 LordHydra. All Rights Reserved.
# Proprietary & Confidential. Do not copy, share, or modify.
