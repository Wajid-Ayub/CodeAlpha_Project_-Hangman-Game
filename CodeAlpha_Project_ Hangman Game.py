import random  # Used to pick random words for the game
import time   # Helps track how long the game takes
import tkinter as tk  # Library for creating the graphical user interface (GUI)
from tkinter import messagebox  # For showing pop-up messages like win/lose alerts

class HangmanGUI:
    def __init__(self, root):
        # Initialize the main window
        self.root = root  # The main window object
        self.root.title("Hangman Game")  # Set the window title
        self.root.geometry("600x700")  # Set window size to 600px wide, 700px tall
        self.root.configure(bg="#f0f0f0")  # Set background color to light gray

        # Word lists by difficulty
        self.easy_words = ['cat', 'dog', 'bird', 'fish', 'tree']  # Simple 3-4 letter words
        self.medium_words = ['python', 'computer', 'network', 'software', 'interface']  # 6-8 letter words
        self.hard_words = ['algorithm', 'programming', 'developer', 'javascript', 'database']  # 9+ letter words

        # Hangman visuals
        self.hangman_pics = [  # List of ASCII art for each stage of the hangman
            "  +---+\n      |\n      |\n      |\n     ===",  # Stage 0: Empty gallows
            "  +---+\n  O   |\n      |\n      |\n     ===",  # Stage 1: Head added
            "  +---+\n  O   |\n  |   |\n      |\n     ===",  # Stage 2: Body added
            "  +---+\n  O   |\n /|   |\n      |\n     ===",  # Stage 3: Left arm
            "  +---+\n  O   |\n /|\\  |\n      |\n     ===",  # Stage 4: Right arm
            "  +---+\n  O   |\n /|\\  |\n /    |\n     ===",  # Stage 5: Left leg
            "  +---+\n  O   |\n /|\\  |\n / \\  |\n     ==="   # Stage 6: Right leg (game over)
        ]

        # Game variables
        self.total_score = 0  # Tracks points across all games
        self.reset_game()  # Set up initial game state

        # GUI Elements
        self.create_widgets()  # Build the interface

    def create_widgets(self):
        # Title
        tk.Label(self.root, text="Hangman Game", font=("Arial", 24, "bold"), 
                bg="#f0f0f0", fg="#333333").pack(pady=10)  # Big title at the top, dark gray text

        # Difficulty selection
        self.difficulty_frame = tk.Frame(self.root, bg="#f0f0f0")  # Container for difficulty options
        self.difficulty_frame.pack(pady=10)  # Add it to the window with padding
        tk.Label(self.difficulty_frame, text="Choose Difficulty:", 
                font=("Arial", 12), bg="#f0f0f0").pack()  # Label above radio buttons
        
        difficulties = [("Easy", 1), ("Medium", 2), ("Hard", 3)]  # Options for difficulty
        self.difficulty_var = tk.IntVar(value=1)  # Variable to track chosen difficulty, default to 1 (Easy)
        for text, value in difficulties:
            tk.Radiobutton(self.difficulty_frame, text=text, value=value, 
                         variable=self.difficulty_var, command=self.start_game,
                         bg="#f0f0f0", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)  # Add each radio button

        # Hangman display
        self.hangman_label = tk.Label(self.root, text=self.hangman_pics[0], 
                                    font=("Courier", 14), bg="#f0f0f0", justify="left")  # Show hangman art
        self.hangman_label.pack(pady=20)  # Add it with vertical spacing

        # Word display
        self.word_label = tk.Label(self.root, text="", font=("Arial", 20), bg="#f0f0f0")  # Show word progress
        self.word_label.pack(pady=10)  # Add with padding

        # Status display
        self.status_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#f0f0f0")  # Show lives/hints/guesses
        self.status_label.pack(pady=5)  # Add with small padding

        # Guess entry
        self.guess_frame = tk.Frame(self.root, bg="#f0f0f0")  # Container for guess input
        self.guess_frame.pack(pady=10)  # Add it to the window
        tk.Label(self.guess_frame, text="Guess:", font=("Arial", 12), 
                bg="#f0f0f0").pack(side=tk.LEFT, padx=5)  # Label next to entry box
        self.guess_entry = tk.Entry(self.guess_frame, width=10, font=("Arial", 12))  # Text box for guesses
        self.guess_entry.pack(side=tk.LEFT, padx=5)  # Add it next to label
        self.guess_entry.bind("<Return>", lambda event: self.make_guess())  # Press Enter to guess

        # Buttons
        self.button_frame = tk.Frame(self.root, bg="#f0f0f0")  # Container for buttons
        self.button_frame.pack(pady=10)  # Add with padding
        tk.Button(self.button_frame, text="Guess", command=self.make_guess, 
                 bg="#4CAF50", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)  # Green Guess button
        tk.Button(self.button_frame, text="Hint", command=self.use_hint, 
                 bg="#2196F3", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)  # Blue Hint button

        # Score display
        self.score_label = tk.Label(self.root, text="Total Score: 0", 
                                  font=("Arial", 12, "bold"), bg="#f0f0f0")  # Show total points
        self.score_label.pack(pady=10)  # Add with padding

    def reset_game(self):
        # Set up a new game based on difficulty
        difficulty = self.difficulty_var.get() if hasattr(self, 'difficulty_var') else 1  # Get chosen difficulty
        if difficulty == 1:
            self.word_list, self.max_lives = self.easy_words, 7  # Easy: 7 lives
        elif difficulty == 2:
            self.word_list, self.max_lives = self.medium_words, 6  # Medium: 6 lives
        else:
            self.word_list, self.max_lives = self.hard_words, 5  # Hard: 5 lives

        self.word = random.choice(self.word_list)  # Pick a random word
        self.word_letters = set(self.word)  # Unique letters in the word
        self.guessed_letters = set()  # Letters player has guessed
        self.lives = self.max_lives  # Start with full lives
        self.hints_left = 2  # Give 2 hints per game
        self.start_time = time.time()  # Record start time

    def start_game(self):
        # Begin a fresh game
        self.reset_game()  # Reset all variables
        self.update_display()  # Show initial state
        if hasattr(self, 'guess_entry'):
            self.guess_entry.delete(0, tk.END)  # Clear the guess box
            self.guess_entry.focus()  # Put cursor in guess box

    def update_display(self):
        # Refresh the screen with current game state
        self.hangman_label.config(text=self.hangman_pics[self.max_lives - self.lives])  # Update hangman picture
        word_display = ' '.join(letter if letter in self.guessed_letters else '_' 
                              for letter in self.word)  # Show word with underscores
        self.word_label.config(text=word_display)  # Update word display
        status = (f"Lives: {self.lives} | Hints: {self.hints_left} | "
                 f"Guessed: {', '.join(sorted(self.guessed_letters))}")  # Status text
        self.status_label.config(text=status)  # Update status
        self.score_label.config(text=f"Total Score: {self.total_score}")  # Update score

    def use_hint(self):
        # Give a hint if available
        if self.hints_left > 0:  # Check if hints remain
            unguessed = [letter for letter in self.word_letters 
                        if letter not in self.guessed_letters]  # Find unguessed letters
            if unguessed:
                hint = random.choice(unguessed)  # Pick a random unguessed letter
                self.guessed_letters.add(hint)  # Add it to guesses
                self.word_letters.remove(hint)  # Remove from letters to guess
                self.hints_left -= 1  # Use up a hint
                self.update_display()  # Show new state
                if not self.word_letters:
                    self.end_game(True)  # Win if no letters left
            else:
                messagebox.showinfo("Hint", "No more letters to hint!")  # All letters guessed
        else:
            messagebox.showinfo("Hint", "No hints remaining!")  # Out of hints

    def make_guess(self):
        # Process the player's guess
        guess = self.guess_entry.get().lower()  # Get input and make it lowercase
        self.guess_entry.delete(0, tk.END)  # Clear the input box
        
        if not guess or len(guess) != 1 or guess not in 'abcdefghijklmnopqrstuvwxyz':
            messagebox.showwarning("Invalid Input", "Please enter a single letter!")  # Bad input
            return
        if guess in self.guessed_letters:
            messagebox.showinfo("Repeated Guess", "You already guessed that letter!")  # Already guessed
            return

        self.guessed_letters.add(guess)  # Add new guess
        if guess in self.word_letters:
            self.word_letters.remove(guess)  # Correct guess
        else:
            self.lives -= 1  # Wrong guess, lose a life
        
        self.update_display()  # Update screen
        
        if not self.word_letters:
            self.end_game(True)  # Win if all letters guessed
        elif self.lives <= 0:
            self.end_game(False)  # Lose if no lives left

    def end_game(self, won):
        # Handle game end
        game_time = round(time.time() - self.start_time, 1)  # Calculate play time
        if won:
            score = self.lives * 100 + self.hints_left * 50  # Points: 100 per life, 50 per hint
            self.total_score += score  # Add to total
            msg = (f"You won in {game_time}s!\nWord: {self.word}\n"
                  f"Score: {score} (Lives: {self.lives}x100 + Hints: {self.hints_left}x50)")  # Win message
        else:
            msg = f"Game Over! Word was: {self.word}\nTime: {game_time}s"  # Lose message

        play_again = messagebox.askyesno("Game Over", f"{msg}\n\nPlay again?")  # Ask to replay
        self.update_display()  # Show final state
        if play_again:
            self.start_game()  # Start new game
        else:
            self.root.quit()  # Close window

if __name__ == "__main__":
    # Main program entry point
    root = tk.Tk()  # Create the main window
    app = HangmanGUI(root)  # Create game instance
    root.mainloop()  # Start the game loop