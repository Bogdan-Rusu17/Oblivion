import pygame, assets, json
import sys
from game import Game
from button import Button

# screen details

# background details
background = None
titleText = None

# Define colors

class Menu:
    def __init__(self):
        global background, titleText

        self.buttons = [
            Button("New Game", 5 * assets.width / 6, 3 * assets.height / 4 - 2 * assets.height / 17, self.play_new_game),
            Button("Load Game", 5 * assets.width / 6, 3 * assets.height / 4 - assets.height / 17, self.play_old_game),
            Button("Settings", 5 * assets.width / 6, 3 * assets.height / 4),
            Button("Quit", 5 * assets.width / 6, 3 * assets.height / 4 + assets.height / 17, Button.quit_game)
        ]

        background = pygame.image.load('../graphics/menu/menu_bg.png').convert_alpha()
        background = pygame.transform.scale(background, (assets.width, assets.height))
        titleText = pygame.image.load('../graphics/menu/game_title.png').convert_alpha()
        titleText = pygame.transform.scale(titleText, (assets.width / 2, assets.height / 2))

    def draw(self):
        # Draw background
        assets.screen.blit(background, (0, 0))

        # # Draw title
        titleRect = titleText.get_rect(center=(assets.width / 2, assets.height / 4))
        assets.screen.blit(titleText, titleRect)

        # # Draw buttons
        for button in self.buttons:
            button.draw()

    def check_events(self, position):
        for button in self.buttons:
            if button.is_hovered(position):
                button.click()
    
    @staticmethod
    def play_old_game():
        flag = 'load'
        game = Game(flag)
        game.run()

    @staticmethod
    def play_new_game():
        flag = 'new'
        game = Game(flag)
        game.run()
    
    def run(self):
        assets.menuMusic.play(loops = -1)
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
