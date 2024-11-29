import pygame
import random
from board import MansionBoard
from game_logic import Game
from player import Player

def roll_dice():
    #Six-sided dice.
    return random.randint(1, 6)

def show_intro(screen, screen_width, screen_height):
    #Intro Message

    pygame.font.init()
    font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 28)

    # Intro text
    intro_text = [
        "Welcome to Cluedo! The murder mystery game...",
        "A murder has been committed in the mansion.",
        "Your task: Find out who the murderer is, where the crime took place, and the weapon used.",
        "But be careful - TIME IS RUNNING OUT!"
    ]

    screen.fill((0, 0, 0))

    for i, line in enumerate(intro_text):
        text = font.render(line, True, (254, 254, 254))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 100 + i * 60))
        screen.blit(text, text_rect)


    hint_text = small_font.render("Press ENTER to begin", True, (255, 255, 255))
    hint_rect = hint_text.get_rect(center=(screen_width // 2, screen_height - 100))
    screen.blit(hint_text, hint_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def render_room_image(screen, room_name, weapon_hint, board, screen_width, screen_height):

    #Display the image of the room the player enters and a hint about the weapon in the room.
    
    room_image_path = board.room_images.get(room_name)
    try:
        room_image = pygame.image.load(room_image_path)
        room_image = pygame.transform.scale(room_image, (screen_width // 2, screen_height // 2))
    except FileNotFoundError:
        print(f"Error: Image file {room_image_path} not found.")
        room_image = pygame.Surface((screen_width // 2, screen_height // 2))
        room_image.fill((255, 0, 0))  # Red placeholder for missing image

    room_image_rect = room_image.get_rect(center=(screen_width // 2, screen_height // 3))

    
    screen.fill((0, 0, 0))  
    screen.blit(room_image, room_image_rect)

    
    font = pygame.font.Font(None, 36)
    hint_text = font.render(f"Hint: {weapon_hint} weapon is in this room.", True, (255, 255, 255))
    hint_text_rect = hint_text.get_rect(center=(screen_width // 2, screen_height // 1.2))
    screen.blit(hint_text, hint_text_rect)

    pygame.display.flip()
    pygame.time.delay(3000)  

def render_note_sheet(screen, suggestions_made, room_weapons, screen_width, screen_height):
    
    #Detective's Note Sheet showing past suggestions and room-weapon information.

    screen.fill((0, 0, 0))  

    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 28)
    title = font.render("Detective's Note Sheet", True, (255, 255, 255))
    screen.blit(title, (screen_width // 2 - 200, 50))

    # Display past suggestions
    suggestion_title = small_font.render("Suggestions Made:", True, (255, 255, 255))
    screen.blit(suggestion_title, (100, 120))

    if suggestions_made:
        for i, suggestion in enumerate(suggestions_made):
            suggestion_text = small_font.render(suggestion, True, (255, 255, 255))
            screen.blit(suggestion_text, (100, 150 + i * 30))
    else:
        no_suggestions = small_font.render("No suggestions made yet.", True, (255, 255, 255))
        screen.blit(no_suggestions, (100, 150))

    # Display message of what weapon is in the room.
    room_weapons_title = small_font.render("Room Weapon Hints:", True, (255, 255, 255))
    screen.blit(room_weapons_title, (screen_width // 2 + 50, 120))

    for i, (room, weapon) in enumerate(room_weapons.items()):
        room_text = small_font.render(f"{room}: {weapon}", True, (255, 255, 255))
        screen.blit(room_text, (screen_width // 2 + 50, 150 + i * 30))

    # Display exit instruction
    exit_message = small_font.render("Press L to return to the game", True, (255, 255, 255))
    screen.blit(exit_message, (screen_width // 2 - 150, screen_height - 50))

    pygame.display.flip()

def render_suggestions(screen, font, suggestion_font, suggestion_phase, selected_character, selected_weapon, characters, weapons, screen_width, screen_height):
    """
    Render the suggestion options during the suggestion phase with a black background.
    """
    screen.fill((0, 0, 0))  
    # Suggestions: selecting character and weapon within a room.
    if suggestion_phase == 0:  
        suggestion_text = font.render("Select Character", True, (255, 255, 255))
        screen.blit(suggestion_text, (screen_width // 2 - 150, screen_height // 2 - 200))
        for i, character in enumerate(characters):
            color = (255, 255, 255) if i == selected_character else (100, 100, 100)
            option_text = suggestion_font.render(character, True, color)
            screen.blit(option_text, (screen_width // 2 - 100, screen_height // 2 - 150 + i * 40))
    elif suggestion_phase == 1:  # Selecting Weapon
        suggestion_text = font.render("Select Weapon", True, (255, 255, 255))
        screen.blit(suggestion_text, (screen_width // 2 - 150, screen_height // 2 - 200))
        for i, weapon in enumerate(weapons):
            color = (255, 255, 255) if i == selected_weapon else (100, 100, 100)
            option_text = suggestion_font.render(weapon, True, color)
            screen.blit(option_text, (screen_width // 2 - 100, screen_height // 2 - 150 + i * 40))

    pygame.display.flip()

# Instructions for the game 
def render_instructions(screen, screen_width, screen_height):
    """
    Render the game instructions screen.
    """
    screen.fill((0, 0, 0))  

    
    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 28)
    title = font.render("Game Instructions", True, (255, 255, 255))
    screen.blit(title, (screen_width // 2 - 150, 50))

    # Instructions content
    instructions = [
        "1. Roll the dice to move around the mansion.",
        "2. Investigate rooms to gather clues.",
        "3. Make suggestions to narrow down suspects, weapons, and locations.",
        "4. Use the Detective's Note Sheet to track your deductions.",
        "5. Solve the mystery before time runs out!",
    ]

    for i, instruction in enumerate(instructions):
        text = small_font.render(instruction, True, (255, 255, 255))
        screen.blit(text, (100, 150 + i * 40))

    # Display exit instruction
    exit_message = small_font.render("Press I to return to the game", True, (255, 255, 255))
    screen.blit(exit_message, (screen_width // 2 - 150, screen_height - 50))

    pygame.display.flip()

def main():
    pygame.init()

    # Set up full-screen mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Cluedo Game")
    clock = pygame.time.Clock()

    # Get screen dimensions
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h

    # Show the intro message
    show_intro(screen, screen_width, screen_height)

    # Initialize the board, game, and player
    board = MansionBoard()
    board.setup_rooms()
    board.setup_weapons()
    player = Player("Detective", (3, 4))  
    game = Game(board)

    # Font setup for displaying text
    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 28)
    suggestion_font = pygame.font.Font(None, 36)

    # Game variables
    running = True
    instructions_active = False
    note_sheet_active = False
    dice_visible = True
    roll_result = None
    spaces_left_to_move = 0
    current_room = None
    last_room = None
    suggestions_made = []
    room_weapons = {}  
    suggestion_active = False
    suggestion_phase = 0
    selected_character = 0
    selected_weapon = 0
    feedback_timer = 0
    suggestion_feedback = ""

    # Characters and weapons for suggestion
    characters = ["Miss Scarlet", "Professor Plum", "Mrs. Peacock", "Reverend Green", "Colonel Mustard", "Mrs. White"]
    weapons = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif instructions_active and event.key == pygame.K_i:
                    instructions_active = False  # Return to the game
                elif not instructions_active and event.key == pygame.K_i:
                    instructions_active = True  # Show the Game Instructions
                elif note_sheet_active and event.key == pygame.K_l:
                    note_sheet_active = False  # Return to the game
                elif not note_sheet_active and event.key == pygame.K_l:
                    note_sheet_active = True  # Show the Note Sheet
                elif not instructions_active and not note_sheet_active:
                    if event.key == pygame.K_SPACE and dice_visible:
                        roll_result = roll_dice()
                        spaces_left_to_move = roll_result
                        dice_visible = False
                    elif spaces_left_to_move > 0:
                        direction_map = {
                            pygame.K_UP: (-1, 0),
                            pygame.K_DOWN: (1, 0),
                            pygame.K_LEFT: (0, -1),
                            pygame.K_RIGHT: (0, 1),
                        }
                        direction = direction_map.get(event.key)
                        if direction and player.move(direction, board):
                            spaces_left_to_move -= 1
                        if spaces_left_to_move == 0:
                            dice_visible = True
                    elif spaces_left_to_move == 0 and current_room and event.key == pygame.K_s:
                        suggestion_active = True
                        suggestion_phase = 0
                        selected_character = 0
                        selected_weapon = 0
                    elif suggestion_active:
                        if suggestion_phase == 0:
                            if event.key == pygame.K_UP:
                                selected_character = (selected_character - 1) % len(characters)
                            elif event.key == pygame.K_DOWN:
                                selected_character = (selected_character + 1) % len(characters)
                            elif event.key == pygame.K_RETURN:
                                suggestion_phase = 1
                        elif suggestion_phase == 1:
                            if event.key == pygame.K_UP:
                                selected_weapon = (selected_weapon - 1) % len(weapons)
                            elif event.key == pygame.K_DOWN:
                                selected_weapon = (selected_weapon + 1) % len(weapons)
                            elif event.key == pygame.K_RETURN:
                                suggestion = f"{characters[selected_character]} with {weapons[selected_weapon]} in {current_room}"
                                suggestions_made.append(suggestion)
                                suggestion_active = False

                                if (
                                    characters[selected_character] == game.solution["murderer"]
                                    and weapons[selected_weapon] == game.solution["weapon"]
                                    and current_room == game.solution["room"]
                                ):
                                    suggestion_feedback = f"Your suggestion '{suggestion}' is CORRECT!"
                                else:
                                    suggestion_feedback = f"Your suggestion '{suggestion}' is INCORRECT."
                                feedback_timer = pygame.time.get_ticks()

        for room_name, info in board.rooms.items():
            if info["position"] == player.position:
                current_room = room_name
                break
        else:
            current_room = None

        if current_room and current_room != last_room and spaces_left_to_move == 0:
            last_room = current_room
            weapon_in_room = board.rooms[current_room]["weapon"]
            room_weapons[current_room] = weapon_in_room
            render_room_image(screen, current_room, weapon_in_room, board, screen_width, screen_height)

        if instructions_active:
            render_instructions(screen, screen_width, screen_height)
        elif note_sheet_active:
            render_note_sheet(screen, suggestions_made, room_weapons, screen_width, screen_height)
        elif suggestion_active:
            render_suggestions(
                screen,
                font,
                suggestion_font,
                suggestion_phase,
                selected_character,
                selected_weapon,
                characters,
                weapons,
                screen_width,
                screen_height,
            )
        elif suggestion_feedback:
            screen.fill((0, 0, 0))
            feedback_color = (255, 0, 0) if "CORRECT" in suggestion_feedback else (0, 255, 0)
            feedback_text = font.render(suggestion_feedback, True, feedback_color)
            feedback_rect = feedback_text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(feedback_text, feedback_rect)
            pygame.display.flip()

            if pygame.time.get_ticks() - feedback_timer > 3000:
                suggestion_feedback = ""
        else:
            screen.fill((0, 0, 0))
            board.render(screen, screen_width, screen_height)
            board.render_labels(screen, screen_width, screen_height)
            player.render(screen, screen_width, screen_height)

            note_sheet_text = small_font.render("Press L to see The Detective's Note Sheet", True, (0, 0, 0))
            instructions_text = small_font.render("Press I for Game Instructions", True, (0, 0, 0))
            screen.blit(note_sheet_text, (10, 10))
            screen.blit(instructions_text, (10, 40))

            if dice_visible:
                dice_label = font.render("Press SPACE to roll dice", True, (0, 0, 0))
                screen.blit(dice_label, (screen_width // 2 - 200, screen_height - 120))
            if spaces_left_to_move > 0:
                move_text = small_font.render(f"Spaces left: {spaces_left_to_move}", True, (0, 0, 0))
                screen.blit(move_text, (screen_width // 2 - 100, screen_height - 100))
            elif spaces_left_to_move == 0 and current_room:
                suggestion_text = font.render("Press S to make a suggestion", True, (0, 0, 0))
                screen.blit(suggestion_text, (screen_width // 2 - 200, screen_height - 50))

            pygame.display.flip()
            clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
