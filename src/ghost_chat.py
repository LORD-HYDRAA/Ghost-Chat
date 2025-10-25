

import sys
import os
import socket
import threading
import time
import argparse
import signal
import readline
import shutil
from typing import Optional, Dict, Any

# © 2025 LordHydra. All Rights Reserved.
# Proprietary & Confidential. Do not copy, share, or modify.
from crypto import GhostCrypto
from network import NetworkManager
from tor_manager import TorManager
from memory_manager import MemoryManager


class GhostChat:
    def __init__(self, args):
        self.args = args
        self.mode = args.mode
        self.username = args.username
        self.is_running = True
        self.messages = []  
        
       
        self.crypto = GhostCrypto(
            outer_key=args.outer_key,
            inner_key=args.inner_key,
            chat_key=args.chat_key
        )
        
        self.network = NetworkManager(port=args.port)
        self.tor_manager = TorManager(control_port=args.tor_port)
        self.memory_manager = MemoryManager()
        
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals to ensure memory cleanup"""
        print(f"\n\033[91m[!] Received signal {signum}. Shutting down securely...\033[0m")
        self.secure_shutdown()
        
    def secure_shutdown(self):
        """Securely wipe all sensitive data from memory"""
        self.is_running = False
        
        
        self.memory_manager.secure_wipe(self.messages)
        self.crypto.wipe_keys()
        self.network.close()
        self.tor_manager.cleanup()
        
      
        import gc
        gc.collect()
        
        
        os.system('echo -ne "\033]10;#ffffff\007"')
        os.system('echo -ne "\033]11;#000000\007"')
        
        print("\033[92m[+] All data securely wiped from memory. Goodbye!\033[0m")
        sys.exit(0)
    
    def display_banner(self):
        """Display Lord Hydra Ghost Chat banner, always centered"""
      
        os.system('echo -ne "\033]10;#00ff00\007"')
        os.system('echo -ne "\033]11;#000000\007"')
        os.system('clear')

        banner = """\033[92m
 ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗         ██████╗██╗  ██╗ █████╗ ████████╗    
██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝        ██╔════╝██║  ██║██╔══██╗╚══██╔══╝    
██║  ███╗███████║██║   ██║███████╗   ██║           ██║     ███████║███████║   ██║       
██║   ██║██╔══██║██║   ██║╚════██║   ██║           ██║     ██╔══██║██╔══██║   ██║       
╚██████╔╝██║  ██║╚██████╔╝███████║   ██║           ╚██████╗██║  ██║██║  ██║   ██║       
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝            ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝       
\033[96m
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
     TEMPORARY • PRIVATE • DECENTRALIZED • FREEDOM  
      Great power comes with Great responsibility 
      Created by Lord Hydra (Mohammed Zaid Khan) 
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
\033[0m
"""

        lines = banner.splitlines()
        terminal_width = shutil.get_terminal_size((80, 20)).columns

        os.system('clear')
        for line in lines:
            print(line.center(terminal_width))

        print(f"\033[92mMode: {self.mode.upper()}\033[0m".center(terminal_width))
        print(f"\033[92mUser: {self.username}\033[0m".center(terminal_width))
        print("\033[91mType '/exit' to leave chat securely\033[0m".center(terminal_width))
        print("\033[90m" + "─" * terminal_width + "\033[0m")
    
    def handle_user_input(self):
        """Handle user input in a separate thread"""
        while self.is_running:
            try:
                message = input("\033[92mYou: \033[0m").strip()
                
                if not message:
                    continue
                    
                if message.lower() == '/exit':
                    self.secure_shutdown()
                    break
                    
                elif message.lower() == '/help':
                    self.show_help()
                    
                elif message.lower() == '/status':
                    self.show_status()
                    
                else:
                    encrypted_msg = self.crypto.encrypt_message(message, self.username)
                    if encrypted_msg:
                        self.network.send_message(encrypted_msg)
                        
            except EOFError:
                break
            except Exception as e:
                print(f"\033[91m[!] Input error: {e}\033[0m")
    
    def handle_incoming_messages(self):
        """Handle incoming messages in a separate thread"""
        while self.is_running:
            try:
                encrypted_msg = self.network.receive_message()
                if encrypted_msg:
                    decrypted_msg = self.crypto.decrypt_message(encrypted_msg)
                    if decrypted_msg:
                        self.display_message(decrypted_msg)
            except Exception as e:
                if self.is_running:
                    print(f"\033[91m[!] Receive error: {e}\033[0m")
    
    def display_message(self, message_data: Dict[str, Any]):
        """Display a received message"""
        username = message_data.get('username', 'Unknown')
        message = message_data.get('message', '')
        timestamp = message_data.get('timestamp', time.time())
        formatted_time = time.strftime('%H:%M:%S', time.localtime(timestamp))
        
        user_colors = ['\033[93m', '\033[96m', '\033[95m', '\033[94m']
        user_color = user_colors[hash(username) % len(user_colors)]
        
        print(f"{user_color}[{formatted_time}] {username}: {message}\033[0m")
        self.messages.append(message_data)
    
    def show_help(self):
        """Show available commands"""
        help_text = """
\033[96mGhost Chat Commands:
/exit    - Securely exit and wipe all data
/help    - Show this help message  
/status  - Show connection status
\033[0m
"""
        print(help_text)
    
    def show_status(self):
        """Show current connection status"""
        status = f"""
\033[96mStatus:
- Connected: {self.network.is_connected()}
- Mode: {self.mode}
- Messages in memory: {len(self.messages)}
- Encryption: {self.crypto.get_status()}
\033[0m
"""
        print(status)
    
    def host_chat(self):
        """Start hosting a chat session"""
        print("\033[92m[+] Starting as host...\033[0m")
        
        onion_address = self.tor_manager.create_hidden_service(self.args.port)
        if not onion_address:
            print("\033[91m[!] Failed to create Tor hidden service\033[0m")
            return False
            
        print(f"\033[92m[+] Hidden service created: {onion_address}.onion\033[0m")
        print("\033[92m[+] Share this address with your chat partner\033[0m")
        
        if not self.network.start_listening():
            return False
            
        print("\033[92m[+] Waiting for connections...\033[0m")
        return True
    
    def join_chat(self):
        """Join an existing chat session"""
        print(f"\033[92m[+] Joining chat at {self.args.onion_address}...\033[0m")
        
        if not self.network.connect_to_host(self.args.onion_address):
            return False
            
        print("\033[92m[+] Connected to chat!\033[0m")
        return True
    
    def run(self):
        """Main chat loop"""
        self.display_banner()
        
        try:
            success = self.host_chat() if self.mode == "host" else self.join_chat()
            if not success:
                print("\033[91m[!] Failed to initialize chat session\033[0m")
                return
            
            input_thread = threading.Thread(target=self.handle_user_input, daemon=True)
            receive_thread = threading.Thread(target=self.handle_incoming_messages, daemon=True)
            input_thread.start()
            receive_thread.start()
            
            while self.is_running:
                time.sleep(1)
                
        except Exception as e:
            print(f"\033[91m[!] Critical error: {e}\033[0m")
        finally:
            self.secure_shutdown()


def main():
    parser = argparse.ArgumentParser(description='Ghost Chat - Secure Temporary Chat')
    parser.add_argument('--mode', choices=['host', 'join'], required=True)
    parser.add_argument('--outer-key', required=True, help='Outer encryption key')
    parser.add_argument('--inner-key', required=True, help='Inner encryption key')
    parser.add_argument('--chat-key', required=True, help='Chat session key')
    parser.add_argument('--username', required=True, help='Your display name')
    parser.add_argument('--onion-address', help='Onion address to join (join mode only)')
    parser.add_argument('--port', type=int, default=9999, help='Chat port')
    parser.add_argument('--tor-port', type=int, default=9050, help='Tor control port')
    
    args = parser.parse_args()
    
    if len(args.outer_key) < 8 or len(args.inner_key) < 8 or len(args.chat_key) < 8:
        print("\033[91m[!] Error: All keys must be at least 8 characters long\033[0m")
        sys.exit(1)
    
    chat = GhostChat(args)
    chat.run()


if __name__ == "__main__":
    main()

# © 2025 LordHydra. All Rights Reserved.
# Proprietary & Confidential. Do not copy, share, or modify.