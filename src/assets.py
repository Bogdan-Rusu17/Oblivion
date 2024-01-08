import pygame
import ctypes

width = None
height = None
screen = None
player = None

def importAssets():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 1: System DPI Aware, 2: Per Monitor DPI Aware
    except AttributeError:
        # Not running on Windows or other issue related to ctypes interaction
        pass

    global width, height, screen
    width, height = pygame.display.list_modes()[0]
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

LEVELS = {'level1': {'Background': 0, 'Level': 2, 'Frost': 3, 'Lava': 4}
          }
    