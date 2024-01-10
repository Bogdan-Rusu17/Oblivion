import pygame, assets
from menu import Menu

class Main():
    def __init__(self):
        pygame.init()
        assets.importAssets()
        pygame.display.set_caption('Oblivion')
        icon = pygame.image.load('../graphics/game_icon.png').convert_alpha()
        icon = pygame.transform.scale(icon, (32, 32))
        pygame.display.set_icon(icon)

    def run(self):
        menu = Menu()
        menu.run()

if __name__ == '__main__':
    main = Main()
    main.run()