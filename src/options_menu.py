import pygame, assets
from button import Button

class OptionsMenu():
    def __init__(self):
        # Create buttons for the menu
        self.buttons = [
            Button("Save", assets.width // 2, assets.height // 2, action = Button.save_game),
            Button("Quit", assets.width // 2, assets.height // 2 + assets.height / 17, action = Button.quit_game)
        ]
        self.active = False  # Indicates if the menu is currently active

    def draw(self):
        # Draw the menu buttons if the menu is active
        if self.active:
            for button in self.buttons:
                button.draw()

    def handle_event(self, event):
        # If the menu is active, check for clicks on the buttons
        if self.active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_hovered(mouse_pos):
                        button.click()
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    button.is_hovered(mouse_pos)

    def toggle_menu(self):
        # Toggle the menu's active state
        self.active = not self.active
        pygame.mouse.set_visible(not pygame.mouse.get_visible())