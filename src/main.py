import pygame
from menu import Menu

info = None
width = None
height = None
screen = None

class Main():
    def __init__(self):
        pygame.init()
        global info, width, height, screen
        info = pygame.display.Info()
        width, height = info.current_w, info.current_h
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def run(self):
        menu = Menu(info, width, height, screen)
        menu.run()

if __name__ == '__main__':
    main = Main()
    main.run()