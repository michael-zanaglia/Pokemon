

class KeyListener:

    def __init__(self):
        self.keys: list[int] = []

    def add_keys(self, key):
        if key not in self.keys:
            self.keys.append(key)
        
    def key_pressed(self, key):
        return key in self.keys
    
    def clear(self, key):
        self.keys.clear()