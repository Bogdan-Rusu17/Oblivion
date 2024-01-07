import pygame
import sys
from game import Game

# screen details
info = None
width = None
height = None
screen = None

# background details
background = None
titleText = None

# Define colors
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
LIGHT_GREY = (230, 230, 230)
HOVER_OVERLAY = (200, 200, 200, 200)

class Button:
    def __init__(self, text, x, y, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, 36)
        self.color = WHITE  # Initial color of the text
        self.hover_color = GREY  # Color when mouse hovers over
        self.action = action

        # Load the button frame image
        self.frame_image = pygame.image.load('../graphics/menu/button.png').convert_alpha()

        # Render the text
        self.rendered_text = self.font.render(self.text, True, self.color)
        self.text_rect = self.rendered_text.get_rect(center=(x, y))

        # Adjust the frame size and position based on the text size
        self.frame_rect = self.frame_image.get_rect(center=(x, y))

        self.greyed_frame_image = self.frame_image.copy()
        overlay = pygame.Surface(self.greyed_frame_image.get_size(), pygame.SRCALPHA)
        overlay.fill(HOVER_OVERLAY)
        self.greyed_frame_image.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        self.hovered = False

    def draw(self):
        # Decide which image to use based on hover state
        frame_image_to_use = self.greyed_frame_image if self.hovered else self.frame_image
        screen.blit(frame_image_to_use, self.frame_rect.topleft)

        # Draw the text
        screen.blit(self.rendered_text, self.text_rect)

    def is_hovered(self, position):
        if self.frame_rect.collidepoint(position):
            # Change to hover color and indicate the button is hovered
            self.rendered_text = self.font.render(self.text, True, self.hover_color)
            self.hovered = True
            return True
        else:
            # Change back to normal color and indicate the button is not hovered
            self.rendered_text = self.font.render(self.text, True, self.color)
            self.hovered = False
            return False

    def click(self):
        if self.action:
            self.action()
class Menu:
    def __init__(self, _info, _width, _height, _screen):
        global info, width, height, screen, background, titleText
        info = _info
        width = _width
        height = _height
        screen = _screen

        self.buttons = [
            Button("Play Game", 5 * width / 6, 3 * height / 4 - 60, self.play_game),
            Button("Settings", 5 * width / 6, 3 * height / 4),
            Button("Quit", 5 * width / 6, 3 * height / 4 + 60, self.quit_game)
        ]

        background = pygame.image.load('../graphics/menu/menu_bg.png').convert_alpha()
        background = pygame.transform.scale(background, (width, height))
        titleText = pygame.image.load('../graphics/menu/game_title.png').convert_alpha()
        titleText = pygame.transform.scale(titleText, (width / 2, height / 2))

    def draw(self):
        pass
        # Draw background
        screen.blit(background, (0, 0))

        # # Draw title
        titleRect = titleText.get_rect(center=(width / 2, height / 4))
        screen.blit(titleText, titleRect)

        # # Draw buttons
        for button in self.buttons:
            button.draw()

    def check_events(self, position):
        for button in self.buttons:
            if button.is_hovered(position):
                button.click()

    @staticmethod
    def play_game():
        game = Game(width, height, screen)
        game.run()


    @staticmethod
    def quit_game():
        pygame.quit()
        exit()
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_events(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEMOTION:
                    for button in self.buttons:
                        button.is_hovered(event.pos)

            self.draw()
            pygame.display.update()
