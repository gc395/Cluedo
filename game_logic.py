import random
from player import Player

class Game:
    def __init__(self, board):
        """
        Initialize the game with the given board.
        """
        self.board = board
        self.solution = self.generate_solution()
        self.player = Player("Detective", (3, 4))  # Set initial position
        self.game_clues = []  # Tracks clues the player can discover
        self.distribute_clues()

    def generate_solution(self):
        """
        Generate the hidden murder solution.
        """
        characters = ["Miss Scarlet", "Professor Plum", "Mrs. Peacock", "Reverend Green", "Colonel Mustard", "Mrs. White"]
        weapons = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
        rooms = list(self.board.rooms.keys())

        return {
            "murderer": random.choice(characters),
            "weapon": random.choice(weapons),
            "room": random.choice(rooms),
        }

    def distribute_clues(self):
        """
        Distribute remaining cards between the game's clue pool and the player's hand.
        """
        characters = ["Miss Scarlet", "Professor Plum", "Mrs. Peacock", "Reverend Green", "Colonel Mustard", "Mrs. White"]
        weapons = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
        rooms = list(self.board.rooms.keys())

        all_cards = (
            list(characters) +
            list(weapons) +
            list(rooms)
        )

        # Exclude the solution cards
        all_cards = [card for card in all_cards if card not in self.solution.values()]
        random.shuffle(all_cards)

        # Split cards between the player and the game clues
        self.player.clues = all_cards[:len(all_cards) // 2]
        self.game_clues = all_cards[len(all_cards) // 2:]

    def start_game(self):
        """
        Start the game loop.
        """
        while True:
            # Check if player is inside a room
            current_room = None
            for room_name, info in self.board.rooms.items():
                if info["position"] == self.player.position:
                    current_room = room_name
                    break

            # Display room-specific message
            if current_room:
                print(f"\nYou are in the {current_room}. Press S to make a suggestion.")

            print("\n--- Cluedo Game Menu ---")
            print("1. Move")
            print("2. Make a Suggestion")
            print("3. Make an Accusation")
            print("4. View Your Clues")
            print("5. Quit")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.handle_move()
            elif choice == "2":
                self.handle_suggestion()
            elif choice == "3":
                if self.handle_accusation():
                    print("Congratulations! You solved the mystery!")
                    break
            elif choice == "4":
                print(f"Your clues: {self.player.clues}")
            elif choice == "5":
                print("Thanks for playing!")
                break
            else:
                print("Invalid choice. Please try again.")

    def handle_move(self):
        """
        Handle the player's movement on the board.
        """
        direction = input("Enter direction (up, down, left, right): ").strip().lower()
        directions = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

        if direction in directions:
            if self.player.move(directions[direction], self.board):
                print("You moved successfully!")
            else:
                print("You can't move in that direction.")
        else:
            print("Invalid direction!")

    def handle_suggestion(self):
        """
        Handle the player's suggestion when inside a room.
        """
        current_room = None
        for room_name, info in self.board.rooms.items():
            if info["position"] == self.player.position:
                current_room = room_name
                break

        if not current_room:
            print("You must be in a room to make a suggestion.")
            return

        murderer = input("Who do you suggest is the murderer? ").strip()
        weapon = input(f"What weapon do you suggest (current weapon in {current_room}): ").strip()
        suggestion = [murderer, weapon, current_room]

        # Check for clues that contradict the suggestion
        revealed = [card for card in suggestion if card in self.game_clues]
        if revealed:
            print(f"The game reveals a clue: {random.choice(revealed)}")
        else:
            print("No clues to reveal.")

    def handle_accusation(self):
        """
        Handle the player's accusation.
        """
        murderer = input("Who do you accuse is the murderer? ").strip()
        weapon = input("What weapon do you accuse was used? ").strip()
        room = input("Which room do you accuse the crime took place in? ").strip()

        if (
            murderer == self.solution["murderer"] and
            weapon == self.solution["weapon"] and
            room == self.solution["room"]
        ):
            print("Your accusation is correct!")
            return True
        else:
            print("Your accusation is incorrect!")
            return False
