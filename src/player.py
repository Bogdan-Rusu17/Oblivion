import pygame, assets
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path, collisionSprites):
        super().__init__(groups)

        self.importGraphics(path)
        self.frameIndex = 0
        self.status = 'left_idle'

        self.image = self.animations[self.status][self.frameIndex]
        self.rect = self.image.get_rect()
        
        self.rect = self.rect.inflate(-self.rect.width / 2, -self.rect.height / 3)
        self.rect.topleft = pos
        self.z = assets.LEVELS['level1']['Level']

        # float based movement
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2()
        self.speed = 400

        # collisions
        self.oldRect = self.rect.copy()
        self.collisionSprites = collisionSprites

        # vertical movement
        self.gravity = 15
        self.jump_speed = 1200
        self.onFloor = False
        self.movingFloor = None

    def getStatus(self):
        if self.direction.x == 0 and self.onFloor:
            self.status = self.status.split('_')[0] + '_idle'
        if self.direction.y > 0 and not self.onFloor:
            self.status = self.status.split('_')[0] + '_falling_down'
        if self.direction.y < 0 and not self.onFloor:
            self.status = self.status.split('_')[0] + '_jump_loop'

    def checkContact(self):
        bottomRect = pygame.Rect(0, 0, self.rect.width, 5)
        bottomRect.midtop = self.rect.midbottom
        for sprite in self.collisionSprites.sprites():
            if sprite.rect.colliderect(bottomRect):
                if self.direction.y > 0:
                    self.onFloor = True
                if hasattr(sprite, 'diretion'):
                    self.movingFloor = sprite

    def importGraphics(self, path):
        self.animations = {}
        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(folder[2], key = lambda str: int(str.split('_')[0])):
                    path = folder[0].replace('\\', '/') + '/' + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    surf = pygame.transform.scale(surf, (assets.width / 8, surf.get_height() * assets.width / (8 * surf.get_width())))
                    key = folder[0].split('\\')[1]
                    self.animations[key].append(surf)
        
    def animate(self, dt):
        self.frameIndex += 20 * dt
        if self.frameIndex >= len(self.animations[self.status]):
            self.frameIndex = 0
        self.image = self.animations[self.status][int(self.frameIndex)]

    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right_running'
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left_running'
        else:
            self.direction.x = 0
        
        if keys[pygame.K_SPACE] and self.onFloor:
            self.direction.y = -self.jump_speed

    def collision(self, direction):
        for sprite in self.collisionSprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.rect.left <= sprite.rect.right and self.oldRect.left >= sprite.oldRect.right:
                        self.rect.left = sprite.rect.right
                    if self.rect.right >= sprite.rect.left and self.oldRect.right <= sprite.oldRect.left:
                        self.rect.right = sprite.rect.left
                    self.pos.x = self.rect.x
                else:
                    if self.rect.bottom >= sprite.rect.top and self.oldRect.bottom <= sprite.oldRect.top:
                        self.rect.bottom = sprite.rect.top
                        self.onFloor = True
                    if self.rect.top <= sprite.rect.bottom and self.oldRect.top >= sprite.oldRect.bottom:
                        self.rect.top = sprite.rect.bottom
                    self.pos.y = self.rect.y
                    self.direction.y = 0
        if self.onFloor and self.direction.y != 0:
            self.onFloor = False

    def move(self, dt):
        # horizontal movement
        # if self.direction.x != 0 and self.speed != 0 and dt != 0:
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision('horizontal')

        # vertical movement
        # if self.direction.y != 0 and self.speed != 0 and dt != 0:
        self.direction.y += self.gravity
        self.pos.y += self.direction.y * dt

        # glue player to platform
        if self.movingFloor and self.movingFloor.direction.y > 0 and self.direction.y > 0:
            self.direction.y = 0
            self.rect.bottom = self.movingFloor.rect.top
            self.pos.y = self.rect.y
            self.onFloor = True

        self.rect.y = round(self.pos.y)
        self.collision('vertical')

        self.movingFloor = None
    
    def update(self, dt):
        self.oldRect = self.rect.copy()
        self.input()
        self.getStatus()
        self.move(dt)
        self.checkContact()
        self.animate(dt)

        