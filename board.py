import random
import pygame

class MansionBoard:
    def __init__(self):
        # Define the grid layout
        self.grid = [
            ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
            ['W', 'R1', 'P', 'R2', 'P', 'R3', 'P', 'R4', 'W'],
            ['W', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W'],
            ['W', 'R5', 'P', 'P', 'P', 'P', 'P', 'R6', 'W'],
            ['W', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W'],
            ['W', 'R7', 'P', 'P', 'R8', 'P', 'P', 'R9', 'W'],
            ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ]

        # Define rooms and their initial positions
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
            "Bedroom": "/Users/gesellecancino/Documents/room_images/Bedroom.webp",
            "Bathroom": "/Users/gesellecancino/Documents/room_images/Bath.webp",
            "Study": "/Users/gesellecancino/Documents/room_images/Study.webp",
            "Kitchen": "/Users/gesellecancino/Documents/room_images/Kitchen.webp",
            "Game Room": "/Users/gesellecancino/Documents/room_images/GameRoom.webp",
            "Dining Room": "/Users/gesellecancino/Documents/room_images/DiningRoom.webp",
            "Garage": "/Users/gesellecancino/Documents/room_images/Garage.webp",
            "Courtyard": "/Users/gesellecancino/Documents/room_images/Courtyard.webp",
            "Living Room": "/Users/gesellecancino/Documents/room_images/LivingRoom.webp",
        }

        # Randomly assign positions to the rooms
        self.assign_random_positions()

    def assign_random_positions(self):
        """
        Assign random unique positions to the rooms within the grid.
        """
        rows = len(self.grid)
        cols = len(self.grid[0])

        # Generate all valid positions excluding 'W' (walls) and 'P' (pathways)
        valid_positions = [
            (row_idx, col_idx)
            for row_idx, row in enumerate(self.grid)
            for col_idx, cell in enumerate(row)
            if cell.startswith('R')  # Room slots only
        ]

        # Shuffle and assign unique positions to each room
        random.shuffle(valid_positions)
        for room, position in zip(self.rooms.keys(), valid_positions):
            self.rooms[room]["position"] = position

    def setup_rooms(self):
        """
        Replace room IDs (R1, R2, etc.) in the grid with actual room names.
        """
        for room_name, info in self.rooms.items():
            row, col = info["position"]
            self.grid[row][col] = room_name

    def setup_weapons(self):
        """
        Randomly assign weapons to rooms.
        """
        weapons = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
        random.shuffle(weapons)

        # Assign a weapon to each room
        for room, weapon in zip(self.rooms.keys(), weapons):
            self.rooms[room]["weapon"] = weapon

    def render(self, screen, screen_width, screen_height):
        """
        Render the mansion grid on the pygame screen, scaling to full-screen.
        """
        rows = len(self.grid)
        cols = len(self.grid[0])
        cell_width = screen_width // cols
        cell_height = screen_height // rows

        colors = {
            "W": (210, 180, 140),  # Walls
            "P": (240, 234, 214),  # Pathways
            "Bedroom": (173, 216, 230),  # Example room colors
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
                color = colors.get(cell, (0, 0, 0))  # Default to black
                pygame.draw.rect(
                    screen,
                    color,
                    (col_idx * cell_width, row_idx * cell_height, cell_width, cell_height),
                )
                # Draw grid lines for visual clarity
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    (col_idx * cell_width, row_idx * cell_height, cell_width, cell_height),
                    1,
                )

    def render_labels(self, screen, screen_width, screen_height):
        """
        Render the room labels in the center of each room, scaling to full-screen.
        """
        rows = len(self.grid)
        cols = len(self.grid[0])
        cell_width = screen_width // cols
        cell_height = screen_height // rows

        font = pygame.font.Font(None, int(min(cell_width, cell_height) // 4))  # Dynamically scale font size
        text_color = (0, 0, 0)  # Black text

        for room_name, info in self.rooms.items():
            row, col = info["position"]
            x = col * cell_width + cell_width // 2
            y = row * cell_height + cell_height // 2

            # Render the text
            text = font.render(room_name, True, text_color)
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)
