"""
Encryption module for Ghost Chat
Handles the three-layer encryption system
"""

import os
import base64
import json
import time
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import nacl.secret
import nacl.utils
from custom_mappings import CustomMapping


class GhostCrypto:
    def __init__(self, outer_key: str, inner_key: str, chat_key: str):
        self.outer_key = outer_key
        self.inner_key = inner_key
        self.chat_key = chat_key
        self.fernet = None
        self.nacl_box = None
        self.custom_mapper = CustomMapping(outer_key, inner_key, chat_key)
        
        self.initialize_encryption()
    
    def initialize_encryption(self):
        """Initialize all encryption layers"""
        # Layer 1: AES-256 (Fernet)
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.outer_key.encode()))
        self.fernet = Fernet(key)
        
        # Layer 2: NaCl (using secret box for symmetric encryption)
        nacl_key = hashes.Hash(hashes.SHA256())
        nacl_key.update(self.inner_key.encode())
        nacl_digest = nacl_key.finalize()
        nacl_key_final = nacl_digest[:nacl.secret.SecretBox.KEY_SIZE]
        self.nacl_box = nacl.secret.SecretBox(nacl_key_final)
    
    def custom_mapping_layer(self, data: str) -> str:
        """Layer 3: User-defined creative mapping"""
        return self.custom_mapper.encode(data)
    
    def reverse_mapping_layer(self, data: str) -> str:
        """Reverse the custom mapping layer"""
        return self.custom_mapper.decode(data)
    
    def encrypt_message(self, message: str, username: str) -> Optional[str]:
        """Encrypt a message using all three layers"""
        try:
            # Prepare message data
            message_data = {
                'username': username,
                'message': message,
                'timestamp': time.time()
            }
            
            # Convert to JSON
            json_data = json.dumps(message_data)
            
            # Layer 3: Custom mapping (Creative word substitution)
            mapped_data = self.custom_mapping_layer(json_data)
            
            # Layer 2: NaCl encryption
            if self.nacl_box is None:
                raise ValueError("NaCl box not initialized")
            nacl_encrypted = self.nacl_box.encrypt(mapped_data.encode())
            # © 2025 LordHydra. All Rights Reserved.
# Proprietary & Confidential. Do not copy, share, or modify.
            
            # Layer 1: AES encryption
            if self.fernet is None:
                raise ValueError("Fernet not initialized")
            final_encrypted = self.fernet.encrypt(nacl_encrypted)
            
            return base64.urlsafe_b64encode(final_encrypted).decode()
            
        except Exception as e:
            print(f"[!] Encryption error: {e}")
            return None
    
    def decrypt_message(self, encrypted_data: str) -> Optional[Dict[str, Any]]:
        """Decrypt a message using all three layers"""
        try:
            # Decode base64
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            
            # Layer 1: AES decryption
            if self.fernet is None:
                raise ValueError("Fernet not initialized")
            nacl_encrypted = self.fernet.decrypt(encrypted_bytes)
            
            # Layer 2: NaCl decryption
            if self.nacl_box is None:
                raise ValueError("NaCl box not initialized")
            mapped_data = self.nacl_box.decrypt(nacl_encrypted).decode()
            
            # Layer 3: Reverse mapping
            json_data = self.reverse_mapping_layer(mapped_data)
            
            
            message_data = json.loads(json_data)
            
            return message_data
            
        except Exception as e:
            print(f"[!] Decryption error: {e}")
            return None
    
    def get_status(self) -> str:
        """Get encryption status"""
        return "Active (AES-256 + NaCl + Creative Mapping)"
    
    def wipe_keys(self):
        """Securely wipe keys from memory"""
        
        self.outer_key = '0' * len(self.outer_key)
        self.inner_key = '0' * len(self.inner_key)
        self.chat_key = '0' * len(self.chat_key)
        self.fernet = None
        self.nacl_box = None

# © 2025 LordHydra. All Rights Reserved.
# Proprietary & Confidential. Do not copy, share, or modify.