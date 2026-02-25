# sample_game.py
import time

def main():
    print("=== Sample Game Started ===")
    
    # Simulate a game loop
    for i in range(5):
        print(f"Game loop iteration {i+1}")
        time.sleep(0.5)  # wait half a second to simulate frame delay
    
    print("Game over! Thanks for playing.")

if __name__ == "__main__":
    main()
    input("Press enter to exit...")
    