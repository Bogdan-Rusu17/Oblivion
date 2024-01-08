import pygame, assets
from menu import Menu

class Main():
    def __init__(self):
        pygame.init()
        assets.importAssets()
        pygame.display.set_caption('Oblivion')
        pygame.display.set_icon(pygame.image.load('../graphics/game_icon.png').convert_alpha())

    def run(self):
        menu = Menu()
        menu.run()

if __name__ == '__main__':
    main = Main()
    main.run()