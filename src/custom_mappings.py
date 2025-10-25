
USER_CUSTOM_MAPPINGS = {
    # Common words mapped to unrelated terms
    'hello': 'quantum_flare',
    'hi': 'neural_pulse', 
    'hey': 'binary_wave',
    'yes': 'affirmative_signal',
    'no': 'negative_echo',
    'ok': 'protocol_alpha',
    'the': 'void_entity',
    'and': 'nexus_bridge',
    'you': 'spectral_self',
    'your': 'quantum_self',
    'are': 'exist_state',
    'is': 'being_state',
    'this': 'local_instance',
    'that': 'remote_instance',
    'with': 'entangled_link',
    'have': 'possess_field',
    'from': 'origin_vector',
    'they': 'plural_entity',
# © 2025 LordHydra. All Rights Reserved.
# Proprietary & Confidential. Do not copy, share, or modify.
    # Questions become cosmic queries
    'what': 'cosmic_query',
    'when': 'temporal_seek',
    'where': 'spatial_locate',
    'why': 'causal_probe',
    'how': 'method_inquire',
    'who': 'identity_scan',
    
    # Emotions as energy states
    'love': 'harmonic_resonance',
    'happy': 'positive_flux',
    'sad': 'entropy_wave',
    'angry': 'plasma_surge',
    'excited': 'quantum_boost',
    
    # Tech terms as sci-fi concepts
    'chat': 'neural_stream',
    'message': 'data_packet',
    'secret': 'occluded_data',
    'password': 'access_rune',
    'key': 'cipher_token',
    'encrypt': 'quantum_shield',
    'decrypt': 'reality_decode',
    'secure': 'null_field',
    'ghost': 'phantom_protocol',
    
    # Time as dimensional concepts
    'now': 'present_tense',
    'today': 'solar_cycle',
    'tomorrow': 'future_phase',
    'yesterday': 'past_echo',
    'time': 'chrono_flow',
    
    # Common phrases as protocols
    'how are you': 'status_query',
    'whats up': 'situation_report',
    'see you': 'reconverge_point',
    'good morning': 'dawn_protocol',
    'good night': 'stasis_mode',
    'be right back': 'temporal_shift',
    'thank you': 'gratitude_signal',
    'you are welcome': 'acknowledge_signal',
    
    # Single letters as elemental symbols
    'a': 'alpha', 'b': 'beta', 'c': 'gamma', 'd': 'delta', 'e': 'epsilon',
    'f': 'zeta', 'g': 'eta', 'h': 'theta', 'i': 'iota', 'j': 'kappa',
    'k': 'lambda', 'l': 'mu', 'm': 'nu', 'n': 'xi', 'o': 'omicron',
    'p': 'pi', 'q': 'rho', 'r': 'sigma', 's': 'tau', 't': 'upsilon',
    'u': 'phi', 'v': 'chi', 'w': 'psi', 'x': 'omega', 'y': 'nabla', 'z': 'partial',
    
    # Numbers as mathematical concepts
    '0': 'null_set', '1': 'unity', '2': 'binary', '3': 'trinity', '4': 'quaternion',
    '5': 'pentad', '6': 'hexagram', '7': 'septenary', '8': 'octave', '9': 'ennead',
    
    # Special characters as operations
    ' ': 'void', '\n': 'line_break', '\t': 'tab_field',
    '.': 'terminus', ',': 'pause', '!': 'exclaim',
    '?': 'interrogate', '@': 'at_sign', '#': 'hash_mark',
    '$': 'currency', '%': 'percentile', '&': 'conjunction',
    '*': 'asterism', '+': 'addition', '-': 'subtraction',
    '=': 'equality', '/': 'division', '\\': 'reverse_slash',
    '|': 'pipe_line', '~': 'tilde_swing', '`': 'back_quote',
    '(': 'left_bound', ')': 'right_bound', '[': 'left_array',
    ']': 'right_array', '{': 'left_set', '}': 'right_set',
    '<': 'less_than', '>': 'greater_than', '"': 'double_quote',
    "'": 'single_quote', ':': 'colon_point', ';': 'semi_colon',

    # Add YOUR custom mappings below - be creative!
    # 'your_word': 'your_creative_code',
    # 'friend': 'ally_unit',
    # 'meeting': 'convergence_point',
    # 'danger': 'threat_level',
}

class CustomMapping:
    def __init__(self, outer_key: str, inner_key: str, chat_key: str):
        self.outer_key = outer_key
        self.inner_key = inner_key  
        self.chat_key = chat_key
        
     
        self.custom_map = USER_CUSTOM_MAPPINGS.copy()
        
    
        self._add_dynamic_mappings()
        
      
        self.reverse_map = {v: k for k, v in self.custom_map.items()}
        
    def _add_dynamic_mappings(self):
        """Add some key-derived mappings to make it harder to crack"""
        
        key_hash = hash(self.chat_key) % 1000
        
       
        dynamic_mappings = {
            'quick': f'velocity_{key_hash}',
            'fast': f'speed_{key_hash+1}',
            'slow': f'inertia_{key_hash+2}',
            'important': f'priority_{key_hash+3}',
            'urgent': f'critical_{key_hash+4}',
        }
        
        self.custom_map.update(dynamic_mappings)
        
    def encode(self, text: str) -> str:
        """
        Encode text using custom mappings with word priority
        """
    
        lower_text = text.lower()
        result = []
        i = 0
        
        while i < len(lower_text):
            
            matched = False
            for length in range(min(20, len(lower_text) - i), 0, -1):
                word = lower_text[i:i+length]
                if word in self.custom_map:
                    result.append(self.custom_map[word])
                    i += length
                    matched = True
                    break
            
            
            if not matched:
                
                orig_char = text[i]
                lower_char = orig_char.lower()
                if lower_char in self.custom_map:
                    result.append(self.custom_map[lower_char])
                else:
                    result.append(orig_char)
                i += 1
        
        return '|'.join(result)  
    
    def decode(self, encoded_text: str) -> str:
        """
        Decode text using reverse mappings
        """
        parts = encoded_text.split('|')
        result = []
        
        for part in parts:
            if part in self.reverse_map:
                result.append(self.reverse_map[part])
            else:
               
                result.append(part)
        
        return ''.join(result)


def test_mappings():
    mapper = CustomMapping("test", "test", "test")
    
    test_phrases = [
        "hello world",
        "how are you",
        "this is a secret message",
        "meet me tomorrow at 5pm",
        "the password is quantum"
    ]
    
    print("Testing Unique Mappings:")
    print("=" * 50)
    
    for phrase in test_phrases:
        encoded = mapper.encode(phrase)
        decoded = mapper.decode(encoded)
        print(f"Original: {phrase}")
        print(f"Encoded:  {encoded}")
        print(f"Decoded:  {decoded}")
        print(f"Success:  {phrase.lower() == decoded.lower()}")
        print("-" * 50)

if __name__ == "__main__":
    test_mappings()

# © 2025 LordHydra. All Rights Reserved.
# Proprietary & Confidential. Do not copy, share, or modify.