"""
Network management for Ghost Chat
Handles socket connections and message transmission
"""

import socket
import threading
import select
from typing import Optional, Callable
# © 2025 LordHydra. All Rights Reserved.
# Proprietary & Confidential. Do not copy, share, or modify.

class NetworkManager:
    def __init__(self, port: int = 9999):
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.connection: Optional[socket.socket] = None
        self.is_connected = False
        self.listener_thread: Optional[threading.Thread] = None
        
    def start_listening(self) -> bool:
        """Start listening for incoming connections"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('127.0.0.1', self.port))
            self.socket.listen(1)
            self.socket.settimeout(1.0)  
            
            def listen_loop() -> None:
                while not self.is_connected:
                    try:
                        conn, addr = self.socket.accept()
                        self.connection = conn
                        self.is_connected = True
                        print(f"[+] Connection established from {addr}")
                    except socket.timeout:
                        continue
                    except Exception as e:
                        if not self.is_connected:
                            print(f"[!] Listen error: {e}")
                        break
            
            self.listener_thread = threading.Thread(target=listen_loop, daemon=True)
            self.listener_thread.start()
            return True
            
        except Exception as e:
            print(f"[!] Failed to start listening: {e}")
            return False
    
    def connect_to_host(self, onion_address: str) -> bool:
        """Connect to a host through Tor proxy"""
        try:

            import socks
            self.socket = socks.socksocket()
            self.socket.set_proxy(socks.SOCKS5, "127.0.0.1", 9050)
            self.socket.settimeout(30)
            
            self.socket.connect((onion_address, self.port))
            self.connection = self.socket
            self.is_connected = True
            return True
            
        except Exception as e:
            print(f"[!] Failed to connect to {onion_address}: {e}")
            return False
    
    def send_message(self, message: str) -> bool:
        """Send a message through the connection"""
        if not self.is_connected or not self.connection:
            print("[!] Not connected to any peer")
            return False
            
        try:

            message_bytes = message.encode('utf-8')
            header = len(message_bytes).to_bytes(4, 'big')
            self.connection.send(header + message_bytes)
            return True
            
        except Exception as e:
            print(f"[!] Failed to send message: {e}")
            self.is_connected = False
            return False
    
    def receive_message(self) -> Optional[str]:
        """Receive a message from the connection"""
        if not self.is_connected or not self.connection:
            return None
            
        try:

            header = self.connection.recv(4)
            if not header:
                self.is_connected = False
                return None
                
            message_length = int.from_bytes(header, 'big')
            

            message_bytes = b''
            while len(message_bytes) < message_length:
                chunk = self.connection.recv(message_length - len(message_bytes))
                if not chunk:
                    self.is_connected = False
                    return None
                message_bytes += chunk
            
            return message_bytes.decode('utf-8')
            
        except socket.timeout:
            return None
        except Exception as e:
            print(f"[!] Receive error: {e}")
            self.is_connected = False
            return None
    
    def is_connected(self) -> bool:
        """Check if connected to a peer"""
        return self.is_connected
    
    def close(self) -> None:
        """Close network connections"""
        self.is_connected = False
        if self.connection:
            try:
                self.connection.close()
            except:
                pass
        if self.socket:
            try:
                self.socket.close()
            except:
                pass

# © 2025 LordHydra. All Rights Reserved.
# Proprietary & Confidential. Do not copy, share, or modify.