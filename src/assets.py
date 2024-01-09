import pygame
import ctypes

width = None
height = None
screen = None
player = None
enemies = None
level = 'level1'

def importAssets():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 1: System DPI Aware, 2: Per Monitor DPI Aware
    except AttributeError:
        # Not running on Windows or other issue related to ctypes interaction
        pass

    global width, height, screen
    width, height = pygame.display.list_modes()[0]
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

LEVELS = {'level1': {'Basics': 0, 'Border': 2, 'Platforms': 3, 'Lava': 4},
          'level2': {'Lava': 4}
          }
LAYERS = {'level1': ['Basics', 'Border', 'Platforms'], 'level2': ['Border', 'Ice']}

POWER = {'level1': 1, 'level2': 2}
    