import random
import pygame


class MansionBoard:
    def __init__(self):
        # Grid Game Layout
        self.grid = [
            ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
            ['W', 'R1', 'P', 'R2', 'P', 'R3', 'P', 'R4', 'W'],
            ['W', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W'],
            ['W', 'R5', 'P', 'P', 'P', 'P', 'P', 'R6', 'W'],
            ['W', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W'],
            ['W', 'R7', 'P', 'P', 'R8', 'P', 'P', 'R9', 'W'],
            ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ]

        # Positions of Rooms
        self.rooms = {
            "Bedroom": {"position": None, "weapon": None},
            "Bathroom": {"position": None, "weapon": None},
            "Study": {"position": None, "weapon": None},
            "Kitchen": {"position": None, "weapon": None},
            "Game Room": {"position": None, "weapon": None},
            "Dining Room": {"position": None, "weapon": None},
            "Garage": {"position": None, "weapon": None},
            "Courtyard": {"position": None, "weapon": None},
            "Living Room": {"position": None, "weapon": None},
        }

        self.room_images = {
            "Bedroom": "room_images/Bedroom.webp",
            "Bathroom": "room_images/Bath.webp",
            "Study": "room_images/Study.webp",
            "Kitchen": "room_images/Kitchen.webp",
            "Game Room": "room_images/GameRoom.webp",
            "Dining Room": "room_images/DiningRoom.webp",
            "Garage": "room_images/Garage.webp",
            "Courtyard": "room_images/Courtyard.webp",
            "Living Room": "room_images/LivingRoom.webp",
        }

        self.hint_spots = {}  
        self.generated_hints = []  
        self.assign_random_positions()

    # Assign random unique positions to the rooms.
    def assign_random_positions(self):
        rows = len(self.grid)
        cols = len(self.grid[0])

        valid_positions = [
            (row_idx, col_idx)
            for row_idx, row in enumerate(self.grid)
            for col_idx, cell in enumerate(row)
            if cell.startswith('R')  # Room slots only
        ]

        random.shuffle(valid_positions)
        for room, position in zip(self.rooms.keys(), valid_positions):
            self.rooms[room]["position"] = position

    # Replace room IDs with the actual room names.
    def setup_rooms(self):
        for room_name, info in self.rooms.items():
            row, col = info["position"]
            self.grid[row][col] = room_name

    # Place murder weapon in the murder room and assign other weapons to the remaining rooms.
    def setup_weapons(self, solution):
        weapons = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
        weapons.remove(solution["weapon"])
        solution_room = solution["room"]
        self.rooms[solution_room]["weapon"] = solution["weapon"]
        remaining_rooms = [room for room in self.rooms.keys() if room != solution_room]
        random.shuffle(remaining_rooms)
        for room, weapon in zip(remaining_rooms, weapons):
            self.rooms[room]["weapon"] = weapon

    # Generate random hints and place them at random positions on the grid.
    def generate_hints(self, solution):
        characters = [
            "Miss Scarlet", "Professor Plum", "Mrs. Peacock",
            "Reverend Green", "Colonel Mustard", "Mrs. White"
        ]
        non_solution_characters = [char for char in characters if char != solution["murderer"]]
        non_solution_rooms = [room for room in self.rooms.keys() if room != solution["room"]]

        # Hints
        self.generated_hints = [
            f"{random.choice(non_solution_characters)} was in the {random.choice(non_solution_rooms)} during the murder.",
            f"A loud noise was heard in the {solution['room']}.",  
            f"Someone saw {random.choice(non_solution_characters)} heading to the {solution['room']}.",
            f"{random.choice(non_solution_characters)} and {solution['murderer']} were seen talking.", 
        ]

        random.shuffle(self.generated_hints)  
        all_positions = [
            (row_idx, col_idx)
            for row_idx, row in enumerate(self.grid)
            for col_idx, cell in enumerate(row)
            if cell == 'P'  
        ]
        random.shuffle(all_positions)

        self.hint_spots = {
            all_positions[i]: self.generated_hints[i]
            for i in range(min(len(all_positions), len(self.generated_hints)))
        }

    def get_hint(self, position):
        return self.hint_spots.get(position, None)

    # Render the mansion grid on the pygame screen
    def render(self, screen, screen_width, screen_height):
        rows = len(self.grid)
        cols = len(self.grid[0])
        cell_width = screen_width // cols
        cell_height = screen_height // rows

        colors = {
            "W": (210, 180, 140),  # Walls
            "P": (240, 234, 214),  # Pathways
            "Bedroom": (173, 216, 230),  # Room colors
            "Bathroom": (173, 216, 230),
            "Study": (173, 216, 230),
            "Kitchen": (173, 216, 230),
            "Game Room": (173, 216, 230),
            "Dining Room": (173, 216, 230),
            "Garage": (173, 216, 230),
            "Courtyard": (173, 216, 230),
            "Living Room": (173, 216, 230),
        }

        # Draw the grid
        for row_idx, row in enumerate(self.grid):
            for col_idx, cell in enumerate(row):
                color = colors.get(cell, (0, 0, 0))  
                pygame.draw.rect(
                    screen,
                    color,
                    (col_idx * cell_width, row_idx * cell_height, cell_width, cell_height),
                )
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    (col_idx * cell_width, row_idx * cell_height, cell_width, cell_height),
                    1,
                )

        # Format Hint spots as " ? " on the grid.
        font = pygame.font.Font(None, int(min(cell_width, cell_height) // 1.5)) 
        question_mark_color = (0, 104, 0)  

        for (row, col), _ in self.hint_spots.items():
            x = col * cell_width + cell_width // 2
            y = row * cell_height + cell_height // 2
            question_mark = font.render("?", True, question_mark_color)
            question_mark_rect = question_mark.get_rect(center=(x, y))
            screen.blit(question_mark, question_mark_rect)

    # Render the room name labels.
    def render_labels(self, screen, screen_width, screen_height):
        rows = len(self.grid)
        cols = len(self.grid[0])
        cell_width = screen_width // cols
        cell_height = screen_height // rows

        font = pygame.font.Font(None, int(min(cell_width, cell_height) // 4))  
        text_color = (0, 0, 0)  # Black text

        for room_name, info in self.rooms.items():
            row, col = info["position"]
            x = col * cell_width + cell_width // 2
            y = row * cell_height + cell_height // 2

            text = font.render(room_name, True, text_color)
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)
