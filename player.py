import pygame

class Player:
    def __init__(self, name, start_position):
        self.name = name
        self.position = start_position  # (row, col) format
        self.color = (255, 0, 0)  # Red for the player

    def render(self, screen, screen_width, screen_height):
        """
        Render the player on the board, scaled dynamically.
        """
        rows = 7  # Number of rows in the grid
        cols = 9  # Number of columns in the grid
        cell_width = screen_width // cols
        cell_height = screen_height // rows

        x = self.position[1] * cell_width + cell_width // 2
        y = self.position[0] * cell_height + cell_height // 2

        pygame.draw.circle(screen, self.color, (x, y), min(cell_width, cell_height) // 4)

    def move(self, direction, board):
        """
        Move the player if the move is valid.
        """
        rows = len(board.grid)
        cols = len(board.grid[0])
        new_row = self.position[0] + direction[0]
        new_col = self.position[1] + direction[1]

        if 0 <= new_row < rows and 0 <= new_col < cols and board.grid[new_row][new_col] != 'W':
            self.position = (new_row, new_col)
            return True  # Move successful
        return False  # Move invalid
