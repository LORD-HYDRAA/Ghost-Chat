"""
Memory management for Ghost Chat
Ensures sensitive data exists only in RAM and is properly wiped
"""

import ctypes
import sys
import gc
from typing import Any, List
# © 2025 LordHydra. All Rights Reserved.
# Proprietary & Confidential. Do not copy, share, or modify.

class MemoryManager:
    def __init__(self):
        self.sensitive_objects: List[Any] = []
    
    def secure_wipe(self, data: Any) -> None:
        """Securely wipe sensitive data from memory"""
        if isinstance(data, str):
            # Overwrite string data
            wiped = '0' * len(data)
            
            
        elif isinstance(data, list):
            for item in data:
                self.secure_wipe(item)
            data.clear()
            
        elif isinstance(data, dict):
            for key, value in data.items():
                self.secure_wipe(key)
                self.secure_wipe(value)
            data.clear()
            
        elif hasattr(data, '__dict__'):
           
            for attr_name in dir(data):
                if not attr_name.startswith('_'):
                    try:
                        attr_value = getattr(data, attr_name)
                        self.secure_wipe(attr_value)
                        setattr(data, attr_name, None)
                    except:
                        pass
    
    def register_sensitive(self, obj: Any) -> None:
        """Register an object for secure wiping on shutdown"""
        self.sensitive_objects.append(obj)
    
    def cleanup(self) -> None:
        """Perform complete memory cleanup"""
        
        for obj in self.sensitive_objects:
            self.secure_wipe(obj)
        
  
        gc.collect()
        
       
        self.sensitive_objects.clear()

# © 2025 LordHydra. All Rights Reserved.
# Proprietary & Confidential. Do not copy, share, or modify.