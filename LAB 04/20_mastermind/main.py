from game import Mastermind

if __name__ == "__main__":
    print("Welcome to Mastermind!")
    print("Select Difficulty: (1) Easy  (2) Normal  (3) Hard")
    
    choice = input("> ").strip()
    mode_map = {"1": "easy", "2": "normal", "3": "hard"}
    mode = mode_map.get(choice, "normal")
    
    # Passes the chosen mode instead of relying on an empty default initialization[cite: 3]
    game = Mastermind(mode=mode)
    game.run()