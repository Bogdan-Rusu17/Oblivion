import pygame
import ctypes

width = None
height = None
screen = None
player = None
enemies = None
level = 'level1'

menuMusic = None
gameMusic = None
buttonClickSound = None
portalSound = None
impAttackSound = None
explosionSound = None
victoryMusic = None
attackMelee = None
attackRanged = None


def importAssets():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 1: System DPI Aware, 2: Per Monitor DPI Aware
    except AttributeError:
        # Not running on Windows or other issue related to ctypes interaction
        pass
    
    global width, height, screen
    width, height = pygame.display.list_modes()[0]
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

    global menuMusic, gameMusic, buttonClickSound, portalSound, impAttackSound, explosionSound, victoryMusic, attackMelee, attackRanged
    menuMusic = pygame.mixer.Sound('../sounds/battleThemeA.mp3')
    gameMusic = pygame.mixer.Sound('../sounds/DungeonOfFate.mp3')
    buttonClickSound = pygame.mixer.Sound('../sounds/Menu Choice.mp3')
    portalSound = pygame.mixer.Sound('../sounds/blessing.ogg')
    impAttackSound = pygame.mixer.Sound('../sounds/lava.flac')
    explosionSound = pygame.mixer.Sound('../sounds/explosion.wav')
    victoryMusic = pygame.mixer.Sound('../sounds/Victory1.mp3')
    attackMelee = pygame.mixer.Sound('../sounds/attackMelee.flac')
    attackRanged = pygame.mixer.Sound('../sounds/ghost.wav')

LEVELS = {'level1': {'Basics': 0, 'Border': 2, 'Platforms': 3, 'Lava': 4},
          'level2': {'Lava': 4}
          }
LAYERS = {'level1': ['Basics', 'Border', 'Platforms'], 'level2': ['Border', 'Ice']}

POWER = {'level1': 1, 'level2': 2}
    