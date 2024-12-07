import random


class Game:
    def __init__(self, board, player):
        """
        Initializes the Cluedo game logic.
        Args:
            board: The MansionBoard object representing the game board.
            player: The Player object representing the player.
        """
        self.board = board
        self.player = player
        self.solution = self.generate_solution()
        self.game_clues = []
        self.feedback_message = ""
        self.feedback_color = (255, 255, 255) 
        self.hint_used = False
        self.hint_spot_feedback = ""
        self.board.setup_weapons(self.solution)  
        self.board.generate_hints(self.solution)  

    # Generate solution for the game randomly.
    def generate_solution(self):
        characters = [
            "Miss Scarlet", "Professor Plum", "Mrs. Peacock",
            "Reverend Green", "Colonel Mustard", "Mrs. White"
        ]
        weapons = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
        rooms = list(self.board.rooms.keys())

        solution = {
            "murderer": random.choice(characters),
            "weapon": random.choice(weapons),
            "room": random.choice(rooms),
        }
        print(f"DEBUG: Solution - {solution}")
        return solution
      
    # Handling Player's Suggestions: Returns True if correct and False otherwise
    def make_suggestion(self, murderer, weapon, room):
        is_correct = (
            murderer == self.solution["murderer"]
            and weapon == self.solution["weapon"]
            and room == self.solution["room"]
        )
        if is_correct:
            self.feedback_message = f"{murderer} with {weapon} in {room} is CORRECT!"
            self.feedback_color = (0, 255, 0)  
            print("DEBUG: Suggestion is correct!")  
            return True 
        else:
            self.feedback_message = f"{murderer} with {weapon} in {room} is INCORRECT."
            self.feedback_color = (255, 0, 0)  
            print("DEBUG: Suggestion is incorrect!")  
            return False  

    # Provides a random hint to the player based on the game clues
    def provide_hint(self):
        if not self.game_clues:
            return "No more hints available."
        hint = random.choice(self.game_clues)
        print(f"DEBUG: Hint Provided - {hint}")
        return f"Hint: {hint}"

    # Checks if the player's current position matches a hint spot and provides the hint.
    def check_hint_spot(self):
        position = self.player.position
        hint = self.board.get_hint(position)
        if hint:
            self.hint_used = True
            self.hint_spot_feedback = hint
            print(f"DEBUG: Hint Spot Found - {hint}")
        else:
            self.hint_spot_feedback = ""

    # Generate Feedback message and color for suggestions being made.
    def get_feedback(self):
        if self.hint_spot_feedback:
            return self.hint_spot_feedback, (255, 255, 0)  
        return self.feedback_message, self.feedback_color

    def reset_feedback(self):
        self.feedback_message = ""
        self.feedback_color = (255, 255, 255)
        self.hint_spot_feedback = ""

    # Checks if the player has solved the mystery. 
    def check_win_condition(self):
        return self.feedback_color == (0, 255, 0)  # Green feedback indicates a win
