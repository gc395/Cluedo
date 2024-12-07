import pygame
import random
from board import MansionBoard
from game_logic import Game
from player import Player


def roll_dice():
    return random.randint(1, 6)

def show_intro(screen, screen_width, screen_height):
    pygame.font.init()
    font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 28)

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


def render_hint(screen, hint, screen_width, screen_height):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 40)
    hint_text = font.render(hint, True, (255, 255, 0))  # Yellow text for hints
    hint_rect = hint_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(hint_text, hint_rect)
    pygame.display.flip()
    pygame.time.delay(3000)

# Displays image of the room and a hint about the weapon in the room, every time player lands on it.
def render_room_image(screen, room_name, weapon_hint, board, screen_width, screen_height):
    room_image_path = board.room_images.get(room_name)
    try:
        room_image = pygame.image.load(room_image_path)
        room_image = pygame.transform.scale(room_image, (screen_width // 2, screen_height // 2))
    except FileNotFoundError:
        print(f"Error: Image file {room_image_path} not found.")
        room_image = pygame.Surface((screen_width // 2, screen_height // 2))
        room_image.fill((255, 0, 0))

    room_image_rect = room_image.get_rect(center=(screen_width // 2, screen_height // 3))

    screen.fill((0, 0, 0))
    screen.blit(room_image, room_image_rect)

    font = pygame.font.Font(None, 36)
    hint_text = font.render(f"Hint: {weapon_hint} weapon is in this room.", True, (255, 255, 255))
    hint_text_rect = hint_text.get_rect(center=(screen_width // 2, screen_height // 1.2))
    screen.blit(hint_text, hint_text_rect)

    pygame.display.flip()
    pygame.time.delay(3000)

# Render the suggestion options during the suggestion phase.
def render_suggestions(
    screen, font, suggestion_font, suggestion_phase, selected_character, selected_weapon,
    characters, weapons, screen_width, screen_height
):
    screen.fill((0, 0, 0))  
    # Selecting a Character
    if suggestion_phase == 0:  
        suggestion_text = font.render("Select Character", True, (255, 255, 255))
        screen.blit(suggestion_text, (screen_width // 2 - 150, screen_height // 2 - 200))
        for i, character in enumerate(characters):
            color = (255, 255, 255) if i == selected_character else (100, 100, 100)
            option_text = suggestion_font.render(character, True, color)
            screen.blit(option_text, (screen_width // 2 - 100, screen_height // 2 - 150 + i * 40))
    elif suggestion_phase == 1:  
        suggestion_text = font.render("Select Weapon", True, (255, 255, 255))
        screen.blit(suggestion_text, (screen_width // 2 - 150, screen_height // 2 - 200))
        for i, weapon in enumerate(weapons):
            color = (255, 255, 255) if i == selected_weapon else (100, 100, 100)
            option_text = suggestion_font.render(weapon, True, color)
            screen.blit(option_text, (screen_width // 2 - 100, screen_height // 2 - 150 + i * 40))

    pygame.display.flip()

#Render Detective's Note Sheet.
def render_note_sheet(screen, suggestions_made, room_weapons, hints_gathered, screen_width, screen_height):
    screen.fill((0, 0, 0))

    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 28)
    title = font.render("Detective's Note Sheet", True, (255, 255, 255))
    screen.blit(title, (screen_width // 2 - 200, 50))

    # Reference list
    reference_title = small_font.render("Reference:", True, (255, 255, 255))
    screen.blit(reference_title, (100, 120))

    characters = ["Miss Scarlet", "Professor Plum", "Mrs. Peacock", "Reverend Green", "Colonel Mustard", "Mrs. White"]
    weapons = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
    rooms = ["Bedroom", "Bathroom", "Study", "Kitchen", "Game Room", "Dining Room", "Garage", "Courtyard", "Living Room"]

    y_offset = 150
    screen.blit(small_font.render("Characters:", True, (255, 255, 255)), (100, y_offset))
    for character in characters:
        screen.blit(small_font.render(character, True, (255, 255, 255)), (120, y_offset + 30))
        y_offset += 30
    y_offset += 40

    screen.blit(small_font.render("Weapons:", True, (255, 255, 255)), (100, y_offset))
    for weapon in weapons:
        screen.blit(small_font.render(weapon, True, (255, 255, 255)), (120, y_offset + 30))
        y_offset += 30
    y_offset += 40

    screen.blit(small_font.render("Locations:", True, (255, 255, 255)), (100, y_offset))
    for room in rooms:
        screen.blit(small_font.render(room, True, (255, 255, 255)), (120, y_offset + 30))
        y_offset += 30

    # Suggestions Section
    suggestion_title = small_font.render("Suggestions Made:", True, (255, 255, 255))
    screen.blit(suggestion_title, (screen_width // 2 + 50, 120))
    suggestion_y_offset = 150
    if suggestions_made:
        for suggestion in suggestions_made:
            suggestion_text = small_font.render(suggestion, True, (255, 255, 255))
            screen.blit(suggestion_text, (screen_width // 2 + 50, suggestion_y_offset))
            suggestion_y_offset += 30
    else:
        no_suggestions = small_font.render("No suggestions made yet.", True, (255, 255, 255))
        screen.blit(no_suggestions, (screen_width // 2 + 50, suggestion_y_offset))

    suggestion_y_offset += 40

    # Hints Section
    hints_title = small_font.render("Hints Gathered:", True, (255, 255, 255))
    screen.blit(hints_title, (screen_width // 2 + 50, suggestion_y_offset))
    suggestion_y_offset += 40

    # Combine room hints and hints gathered from hint spots
    all_hints = [f"The {weapon} is in the {room}." for room, weapon in room_weapons.items()] + hints_gathered

    if all_hints:
        for hint in all_hints:
            hint_text = small_font.render(hint, True, (255, 255, 255))
            screen.blit(hint_text, (screen_width // 2 + 50, suggestion_y_offset))
            suggestion_y_offset += 30
    else:
        no_hints_text = "No hints gathered yet."
        screen.blit(small_font.render(no_hints_text, True, (255, 255, 255)), (screen_width // 2 + 50, suggestion_y_offset))

    exit_message = small_font.render("Press L to return to the game", True, (255, 255, 255))
    screen.blit(exit_message, (screen_width // 2 - 150, screen_height - 50))

    pygame.display.flip()


#Render game instructions screen
def render_instructions(screen, screen_width, screen_height):
    screen.fill((0, 0, 0))  # Black background

    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 28)
    title = font.render("Game Instructions", True, (255, 255, 255))
    screen.blit(title, (screen_width // 2 - 150, 50))

    instructions = [
        "1. Roll the dice to move around the mansion.",
        "2. Move using Arrow Keys on keyboard.",
        "3. Investigate rooms to gather clues.",
        "\t\t Clues are given when you land on a Question Mark tile and when you enter a room.",
        "4. Make suggestions to narrow down suspects, weapons, and locations.",
        "\t\t You may only make suggestions once you enter a room about that room specifically.",
        "5. Use the Detective's Note Sheet to track your deductions.",
        "6. Solve the mystery before time runs out!",
    ]

    for i, instruction in enumerate(instructions):
        text = small_font.render(instruction, True, (255, 255, 255))
        screen.blit(text, (100, 150 + i * 40))

    exit_message = small_font.render("Press I to return to the game", True, (255, 255, 255))
    screen.blit(exit_message, (screen_width // 2 - 150, screen_height - 50))

    pygame.display.flip()


def main():
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Cluedo Game")
    clock = pygame.time.Clock()

    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h

    show_intro(screen, screen_width, screen_height)

    board = MansionBoard()
    board.setup_rooms()
    player = Player("Detective", (3, 4))
    game = Game(board, player)
    board.generate_hints(game.solution)  # Ensure hints are generated

    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 28)
    suggestion_font = pygame.font.Font(None, 36)

    running = True
    game_over = False
    instructions_active = False
    note_sheet_active = False
    dice_visible = True
    roll_result = None
    spaces_left_to_move = 0
    current_room = None
    last_room = None
    hints_gathered = []  
    suggestions_made = []
    room_weapons = {}
    suggestion_active = False
    suggestion_phase = 0
    selected_character = 0
    selected_weapon = 0
    feedback_timer = 0

    characters = ["Miss Scarlet", "Professor Plum", "Mrs. Peacock", "Reverend Green", "Colonel Mustard", "Mrs. White"]
    weapons = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]

    while running:
        if game_over:  
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_i:
                    instructions_active = not instructions_active
                elif event.key == pygame.K_l:
                    note_sheet_active = not note_sheet_active
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
                            # Check for hints
                            hint = board.get_hint(player.position)
                            if hint and hint not in hints_gathered:
                                hints_gathered.append(hint)
                                render_hint(screen, hint, screen_width, screen_height)
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

                                # Check if the suggestion is correct
                                if game.make_suggestion(
                                    characters[selected_character],
                                    weapons[selected_weapon],
                                    current_room
                                ):
                                    # Display victory message and exit
                                    screen.fill((0, 0, 0))
                                    font = pygame.font.Font(None, 60)
                                    victory_text = font.render("Congratulations! You solved the mystery!", True, (0, 255, 0))
                                    victory_rect = victory_text.get_rect(center=(screen_width // 2, screen_height // 2))
                                    screen.blit(victory_text, victory_rect)
                                    pygame.display.flip()
                                    pygame.time.delay(5000)  # Pause for 5 seconds to display the message
                                    running = False
                                    break

                                feedback_timer = pygame.time.get_ticks()

        # Update the current room based on the player's position
        for room_name, info in board.rooms.items():
            if info["position"] == player.position:
                current_room = room_name
                break
        else:
            current_room = None

        # Render room image when entering a new room
        if current_room and current_room != last_room and spaces_left_to_move == 0:
            last_room = current_room
            weapon_in_room = board.rooms[current_room]["weapon"]
            room_weapons[current_room] = weapon_in_room
            render_room_image(screen, current_room, weapon_in_room, board, screen_width, screen_height)
        
        # Render feedback
        if game.feedback_message:    
            feedback_message, feedback_color = game.get_feedback()
            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 40)  # Use a smaller font size
            feedback_text = font.render(feedback_message, True, feedback_color)
            feedback_rect = feedback_text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(feedback_text, feedback_rect)
            pygame.display.flip()

            # Clear feedback after 3 seconds
            if pygame.time.get_ticks() - feedback_timer > 3000:
                game.reset_feedback()
        elif instructions_active:
            render_instructions(screen, screen_width, screen_height)
        elif note_sheet_active:
            render_note_sheet(screen, suggestions_made, room_weapons, hints_gathered, screen_width, screen_height)
        elif suggestion_active:
            render_suggestions(
                screen, font, suggestion_font, suggestion_phase,
                selected_character, selected_weapon,
                characters, weapons, screen_width, screen_height
            )
        else:
            # Main game screen
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