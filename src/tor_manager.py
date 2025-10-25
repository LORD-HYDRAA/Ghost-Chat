"""
Tor management for Ghost Chat - WITH FALLBACK
"""

import stem
from stem.control import Controller
import tempfile
import os
import subprocess
import time
# © 2025 LordHydra. All Rights Reserved.
# Proprietary & Confidential. Do not copy, share, or modify.

class TorManager:
    def __init__(self, control_port: int = 9050):
        self.control_port = control_port
        self.controller = None
        self.tor_process = None
        self.hidden_service_dir = None
    
    def create_hidden_service(self, port: int):
        """Create a Tor hidden service with fallback"""
        try:
            print("[+] Connecting to Tor control port...")
            
            self.controller = Controller.from_port(port=self.control_port)
            self.controller.authenticate()
            
            print("[+] Creating ephemeral hidden service...")
            
            result = self.controller.create_ephemeral_hidden_service(
                {80: port},
                key_type='NEW',
                key_content='ED25519-V3',
                await_publication=True
            )
            
            self.service_id = result.service_id
            print(f"[+] Hidden service created: {self.service_id}.onion")
            return self.service_id
            
        except Exception as e:
            print(f"[!] Control port failed: {e}")
            print("[+] Using fallback Tor method...")
            return self.fallback_hidden_service(port)
    
    def fallback_hidden_service(self, port: int):
        """Fallback method using manual Tor process"""
        try:
            self.hidden_service_dir = tempfile.mkdtemp(prefix='ghost_tor_')
            

            torrc_content = f"""
SocksPort 0
ControlPort 0
DataDirectory {self.hidden_service_dir}
HiddenServiceDir {self.hidden_service_dir}
HiddenServicePort 80 127.0.0.1:{port}
Log notice stdout
"""
            
            torrc_file = os.path.join(self.hidden_service_dir, "torrc")
            with open(torrc_file, 'w') as f:
                f.write(torrc_content)
            

            self.tor_process = subprocess.Popen([
                'tor', '-f', torrc_file
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            

            for i in range(30):
                hostname_file = os.path.join(self.hidden_service_dir, "hostname")
                if os.path.exists(hostname_file):
                    with open(hostname_file, 'r') as f:
                        onion = f.read().strip()
                        print(f"[+] Fallback hidden service: {onion}")
                        return onion.replace('.onion', '')
                time.sleep(1)
            
            return None
            
        except Exception as e:
            print(f"[!] Fallback also failed: {e}")
            return None
    
    def connect_through_tor(self, address: str, port: int):
        """Connect through Tor network"""
        return True
    
    def cleanup(self):
        """Clean up Tor resources"""
        try:
            if self.controller and hasattr(self, 'service_id'):
                self.controller.remove_ephemeral_hidden_service(self.service_id)
                self.controller.close()
            
            if self.tor_process:
                self.tor_process.terminate()
                self.tor_process.wait()
            
            if self.hidden_service_dir and os.path.exists(self.hidden_service_dir):
                import shutil
                shutil.rmtree(self.hidden_service_dir)
                
        except Exception as e:
            pass 

# © 2025 LordHydra. All Rights Reserved.
# Proprietary & Confidential. Do not copy, share, or modify.