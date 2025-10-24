echo -ne "\033]10;#00ff00\007"  
echo -ne "\033]11;#000000\007" 
# © 2025 LordHydra. All Rights Reserved.
# Proprietary & Confidential. Do not copy, share, or modify.

source ghost_env/bin/activate


MODE=""
OUTER_KEY=""
INNER_KEY=""
CHAT_KEY=""
USERNAME=""
TOR_PORT=9050
CHAT_PORT=9999

show_help() {
    echo "Ghost Chat - Secure Temporary Memory-Only Chat"
    echo ""
    echo "Usage:"
    echo "  ./run.sh -host -key <OuterKey> -inner <InnerKey> -chat <ChatKey> -username <name>"
    echo "  ./run.sh -join -key <OuterKey> -inner <InnerKey> -chat <ChatKey> -username <name> -address <onion_address>"
    echo ""
    echo "Options:"
    echo "  -host              Start as host (create chat room)"
    echo "  -join              Join existing chat room"
    echo "  -key <key>         Outer encryption key (required)"
    echo "  -inner <key>       Inner encryption key (required)"
    echo "  -chat <key>        Chat session key (required)"
    echo "  -username <name>   Your display name (required)"
    echo "  -address <addr>    Onion address to join (join mode only)"
    echo "  -port <port>       Chat port (default: 9999)"
    echo "  -torport <port>    Tor control port (default: 9050)"
    echo "  -help              Show this help message"
}


while [[ $# -gt 0 ]]; do
    case $1 in
        -host)
            MODE="host"
            shift
            ;;
        -join)
            MODE="join"
            shift
            ;;
        -key)
            OUTER_KEY="$2"
            shift 2
            ;;
        -inner)
            INNER_KEY="$2"
            shift 2
            ;;
        -chat)
            CHAT_KEY="$2"
            shift 2
            ;;
        -username)
            USERNAME="$2"
            shift 2
            ;;
        -address)
            ONION_ADDRESS="$2"
            shift 2
            ;;
        -port)
            CHAT_PORT="$2"
            shift 2
            ;;
        -torport)
            TOR_PORT="$2"
            shift 2
            ;;
        -help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Validate required arguments
if [[ -z "$MODE" ]]; then
    echo "Error: Must specify -host or -join mode"
    show_help
    exit 1
fi

if [[ -z "$OUTER_KEY" || -z "$INNER_KEY" || -z "$CHAT_KEY" ]]; then
    echo "Error: All three keys (key, inner, chat) are required"
    show_help
    exit 1
fi

if [[ -z "$USERNAME" ]]; then
    echo "Error: Username is required"
    show_help
    exit 1
fi

if [[ "$MODE" == "join" && -z "$ONION_ADDRESS" ]]; then
    echo "Error: Onion address required for join mode"
    show_help
    exit 1
fi


cd src
python ghost_chat.py \
    --mode "$MODE" \
    --outer-key "$OUTER_KEY" \
    --inner-key "$INNER_KEY" \
    --chat-key "$CHAT_KEY" \
    --username "$USERNAME" \
    --onion-address "$ONION_ADDRESS" \
    --port "$CHAT_PORT" \
    --tor-port "$TOR_PORT"


echo -ne "\033]10;#ffffff\007"  
echo -ne "\033]11;#000000\007" 

# © 2025 LordHydra. All Rights Reserved.
# Proprietary & Confidential. Do not copy, share, or modify.
