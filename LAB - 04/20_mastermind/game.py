import random
from logic import feedback

class Mastermind:
    def __init__(self, mode="normal"):
        modes = {
            "easy": {"length": 4, "symbols": "123456", "turns": 10},
            "normal": {"length": 5, "symbols": "12345678", "turns": 12},
            "hard": {"length": 6, "symbols": "123456789", "turns": 15}
        }
        settings = modes.get(mode, modes["normal"])
        
        self.length = settings["length"]
        self.symbols = settings["symbols"]
        self.turns = settings["turns"]
        
        # Generates a code based on selected difficulty rather than hardcoding 4 digits
        self.code = [str(random.choice(self.symbols)) for _ in range(self.length)]
        self.history = []
        self.active = True

    def run(self):
        print(f"\nMastermind — enter {self.length} digits from {self.symbols[0]} to {self.symbols[-1]}.")
        
        while self.active and self.turns > 0:
            if self.history:
                print("\n--- Guess History ---")
                for i, (g, e, p) in enumerate(self.history, 1):
                    print(f"Turn {i}: {g} | Exact: {e}, Partial: {p}")
                print("---------------------")
                
            raw = input(f"{self.turns} turns left > ").strip()
            
            if raw.lower() == "q":
                print("Game aborted.")
                self.active = False
                return
                
            # Validates length and allowed characters before consuming a turn
            if len(raw) != self.length or any(ch not in self.symbols for ch in raw):
                print(f"Invalid! Enter exactly {self.length} digits from {self.symbols[0]} to {self.symbols[-1]}.")
                continue
                
            guess = list(raw)
            exact, partial = feedback(self.code, guess)
            
            self.history.append((raw, exact, partial))
            self.turns -= 1
            
            print(f"Result -> Exact: {exact}, Partial: {partial}")
            
            if exact == self.length:
                print("\nCongratulations! You cracked the code!")
                self.active = False
                return
                
        if self.active:
            print(f"\nGame over! Out of turns. The code was {''.join(self.code)}")
            self.active = False