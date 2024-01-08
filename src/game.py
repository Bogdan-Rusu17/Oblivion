import pygame, sys, assets
from pytmx.util_pygame import load_pygame
from player import Player


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.displaySurface = pygame.display.get_surface()
        self.bg = pygame.image.load('../data/game_data/map_level1.png').convert_alpha()

    def customizeDraw(self, player):
        self.offset.x = player.rect.centerx - assets.width / 2
        self.offset.y = player.rect.centery - assets.height / 2
        # blit surfaces
        self.displaySurface.blit(self.bg, -self.offset)
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offsetRect = sprite.image.get_rect(center = sprite.rect.center)
            offsetRect.center -= self.offset
            self.displaySurface.blit(sprite.image, offsetRect)

class MySprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -self.rect.height / 3)

class Game():
    def __init__(self):
        self.displaySurface = assets.screen
        self.allSprites = AllSprites()
        self.clock = pygame.time.Clock()
        self.setup()
    
    def setup(self):
        tmx_map = load_pygame('../data/game_data/map_level1.tmx')

        # tiles
        for x, y, surface in tmx_map.get_layer_by_name('Platforms').tiles():
            print('da')
            MySprite((x * 64, y * 64), surface, self.allSprites)

        # for obj in tmx_map.get_layer_by_name('Objects'):
        #     MySprite((obj.x, obj.y), obj.image, allSprites)

        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'Player':
                self.player = Player(pos = (obj.x, obj.y),
                                     groups = self.allSprites)
        #     if obj.name == 'Coffin':
        #         Coffin(pos = (obj.x, obj.y),
        #                 groups = self.allSprites,
        #                 path = PATHS['coffin'],
        #                 collisionSprites = self.obstacles)
            
        #     if obj.name == 'Cactus':
        #         Cactus(pos = (obj.x, obj.y),
        #                 groups = self.allSprites,
        #                 path = PATHS['cactus'],
        #                 collisionSprites = self.obstacles)
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick() / 1000

            # update groups
            # self.allSprites.update(dt)
            # draw groups
            self.displaySurface.fill('black')
            self.allSprites.customizeDraw(self.player)

            pygame.display.update()