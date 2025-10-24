echo "🔧 Applying ultimate Tor fix..."
sudo pkill -f tor
sleep 2
# © 2025 LordHydra. All Rights Reserved.
# Proprietary & Confidential. Do not copy, share, or modify.

sudo tor --runasdaemon 1
sleep 3


if pgrep -x "tor" > /dev/null; then
    echo "✅ Tor is running"
else
    echo "❌ Tor failed to start"
    exit 1
fi

echo "🚀 Now run: sudo -E ./run.sh -host -key 'key1' -inner 'key2' -chat 'key3' -username 'Alice'"

#  © 2025 LordHydra. All Rights Reserved.
#  Proprietary & Confidential. Do not copy, share, or modify.
