import pygame, sys, assets, json
from pytmx.util_pygame import load_pygame
from player import Player
from options_menu import OptionsMenu
from tile import Tile, CollisionTile, MovingObject, InvisibleWall, Portal
from enemy import Imp


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.displaySurface = pygame.display.get_surface()
        self.bg = pygame.image.load('../data/game_data/level1/map.png').convert_alpha()

    def customDraw(self, player):
        self.offset.x = player.rect.centerx - assets.width / 2
        self.offset.y = player.rect.centery - assets.height / 2
        # blit surfaces
        self.displaySurface.blit(self.bg, -self.offset)
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.z):
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
    def __init__(self, flag):
        self.displaySurface = assets.screen
        self.clock = pygame.time.Clock()
        
        # ESC menu
        self.optionsMenu = OptionsMenu()

        # groups
        self.allSprites = AllSprites()
        self.collisionSprites = pygame.sprite.Group()
        self.platformSprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.firebolts = pygame.sprite.Group()
        self.portal = pygame.sprite.Sprite()

        # load previous game or start new game
        if flag == 'new':
            self.setup_new()
        elif flag == 'load':
            self.setup_load()
    
    def platformCollisions(self):
        for platform in self.platformSprites.sprites():
            for border in self.platformRects:
                if platform.rect.colliderect(border):
                    if platform.direction.y < 0:
                        platform.rect.top = border.bottom
                        platform.pos.y = platform.rect.y
                        platform.direction.y = 1
                    else:
                        platform.rect.bottom = border.top
                        platform.pos.y = platform.rect.y
                        platform.direction.y = -1
            if platform.rect.colliderect(self.player.rect) and self.player.rect.centery > platform.rect.centery:
                platform.rect.bottom = self.player.rect.top
                platform.pos.y = platform.rect.y
                platform.direction.y = -1

    def setup_new(self):
        self.allSprites = AllSprites()
        self.collisionSprites = pygame.sprite.Group()
        self.platformSprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.firebolts = pygame.sprite.Group()
        self.portal = pygame.sprite.Sprite()

        tmx_map = load_pygame('../data/game_data/level1/' + assets.level + '.tmx')
        # tiles
        for layer in assets.LAYERS[assets.level]:
            for x, y, surface in tmx_map.get_layer_by_name(layer).tiles():
                CollisionTile((x * 64, y * 64), surface, [self.allSprites, self.collisionSprites])
        
        self.invisibleWalls = []
        for obj in tmx_map.get_layer_by_name('InvisibleWalls'):
            self.invisibleWalls.append(InvisibleWall(obj.x, obj.y, obj.width, obj.height, obj.name))

        for layer in ['Lava']:
            for x, y, surface in tmx_map.get_layer_by_name(layer).tiles():
                Tile((x * 64, y * 64), surface, self.allSprites, assets.LEVELS['level1'][layer])

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player(pos = (obj.x, obj.y),
                                     groups = self.allSprites,
                                     path = '../graphics/player',
                                     collisionSprites = self.collisionSprites,
                                     collisionSpells = self.firebolts,
                                     enemies = self.enemies,
                                     invisibleWalls = self.invisibleWalls)   
            if obj.name == 'Imp':
                Imp(pos = (obj.x, obj.y),
                    groups = [self.allSprites, self.enemies, self.firebolts],
                    path = '../graphics/enemies/imp',
                    player = self.player)
            if obj.name == 'Portal':
                self.portal = Portal((obj.x, obj.y), obj.image, self.allSprites)
                
        assets.player = self.player
        assets.enemies = self.enemies

    def setup_load(self):
        self.allSprites = AllSprites()
        self.collisionSprites = pygame.sprite.Group()
        self.platformSprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.firebolts = pygame.sprite.Group()
        self.portal = pygame.sprite.Sprite()
        assets.level = self.load_game_state()['level']
        tmx_map = load_pygame('../data/game_data/level1/' + self.load_game_state()['level'] + '.tmx')
        
        # tiles
        for layer in assets.LAYERS[assets.level]:
            for x, y, surface in tmx_map.get_layer_by_name(layer).tiles():
                CollisionTile((x * 64, y * 64), surface, [self.allSprites, self.collisionSprites])

        self.invisibleWalls = []
        for obj in tmx_map.get_layer_by_name('InvisibleWalls'):
            self.invisibleWalls.append(InvisibleWall(obj.x, obj.y, obj.width, obj.height, obj.name))

        loadState = self.load_game_state()

        for layer in ['Lava']:
            for x, y, surface in tmx_map.get_layer_by_name(layer).tiles():
                Tile((x * 64, y * 64), surface, self.allSprites, assets.LEVELS[loadState['level']][layer])
        self.player = Player(pos = loadState['player']['player_position'],
                             groups = self.allSprites,
                             path = '../graphics/player',
                             collisionSprites = self.collisionSprites,
                             collisionSpells = self.firebolts,
                             enemies = self.enemies,
                             hp = loadState['player']['health'],
                             mp = loadState['player']['mana'],
                             invisibleWalls = self.invisibleWalls)
        assets.player = self.player
        assets.enemies = self.enemies

        for imp in loadState['imps']:
            Imp(pos = (imp['position']),
                    groups = [self.allSprites, self.enemies, self.firebolts],
                    path = '../graphics/enemies/imp',
                    player = self.player,
                    hp = imp['health'])
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Portal':
                self.portal = Portal((obj.x, obj.y), obj.image, self.allSprites)    
        
    
    def load_game_state(self):
        with open('../saved/game_state.json', 'r') as f:
            game_state = json.load(f)
        return game_state

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.optionsMenu.toggle_menu()
                self.optionsMenu.handle_event(event)
            
            dt = self.clock.tick() / 1000
            if self.optionsMenu.active:
                dt = 0

            self.platformCollisions()
            # update groups
            self.allSprites.update(dt)
            # draw groups
            self.displaySurface.fill('black')
            self.allSprites.customDraw(self.player)
            self.optionsMenu.draw()
            
            # treci la niv urmator
            if self.player.rect.colliderect(self.portal):
                word, number = assets.level[:-1], assets.level[-1]
                next_number = str(int(number) + 1)
                assets.level = word + next_number
                self.setup_new()

            pygame.display.update()