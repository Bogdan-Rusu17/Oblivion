import pygame, assets
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path, collisionSprites, collisionSpells, enemies):
        super().__init__(groups)

        self.allSprites = groups
        self.collisionSpells = collisionSpells

        self.importGraphics(path)
        self.frameIndex = 0
        self.status = 'left_idle'

        self.image = self.animations[self.status][self.frameIndex]
        self.rect = self.image.get_rect()
        self.initMidtop = self.rect.midtop
        
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

        # health mechanics
        self.health = 250
        self.mana = 100
        self.attackingMelee = False
        self.attackingSpell = False
        self.attackTime = 0
        self.enemies = enemies
        self.meleeDamage = 10
        self.manaBar = ManaBar(groups, self)
        self.healthBar = HealthBar(groups, self, self.manaBar)

    def detectFireboltCollision(self):
        for sprite in self.collisionSpells.sprites():
            if self.rect.colliderect(sprite):
                self.damage(sprite.amount)
                sprite.kill()
                print(self.health)

    def getStatus(self):
        if self.direction.x == 0 and self.onFloor:
            self.status = self.status.split('_')[0] + '_idle'
        if self.direction.y > 0 and not self.onFloor:
            self.status = self.status.split('_')[0] + '_falling_down'
        if self.direction.y < 0 and not self.onFloor:
            self.status = self.status.split('_')[0] + '_jump_loop'
        if self.attackingMelee:
            self.status = self.status.split('_')[0] + '_slashing'
        if self.attackingSpell:
            self.status = self.status.split('_')[0] + '_throwing'

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
        self.boltSurf = pygame.image.load('../graphics/particles/flame/magic/deathbolt.png')
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
    
    def attackMelee(self):
        for sprite in self.enemies.sprites():
            if self.rect.colliderect(sprite):
                sprite.damage(self.meleeDamage)
    def attackSpell(self):
        self.mana -= 50
        if self.status.split('_')[0] == 'left':
            Deathbolt(pygame.transform.rotate(self.boltSurf, -90), self.rect.topleft, pygame.math.Vector2(-1, 0), self.allSprites, self.enemies)
        if self.status.split('_')[0] == 'right':
            Deathbolt(pygame.transform.rotate(self.boltSurf, 90), self.rect.topright, pygame.math.Vector2(1, 0), self.allSprites, self.enemies)
        

    def animate(self, dt):
        self.frameIndex += 20 * dt

        if self.attackingMelee and int(self.frameIndex) == 7:
            self.attackMelee()
            self.attackingMelee = False
            self.attackTime = pygame.time.get_ticks()
        
        if self.attackingSpell and int(self.frameIndex) == 7:
            self.attackSpell()
            self.attackingSpell = False
            self.attackTime = pygame.time.get_ticks()

        if self.frameIndex >= len(self.animations[self.status]):
            self.frameIndex = 0
            self.attackingMelee = False
            self.attackingSpell = False
            
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

        if keys[pygame.K_1] and pygame.time.get_ticks() - self.attackTime > 300 and not self.attackingMelee:
            self.attackingMelee = True
            self.frameIndex = 0
        if keys[pygame.K_2] and pygame.time.get_ticks() - self.attackTime > 300 and not self.attackingSpell and self.mana > 50:
            self.attackingSpell = True
            self.frameIndex = 0

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
    
    def damage(self, amount):
        self.health -= amount

    def update(self, dt):
        self.oldRect = self.rect.copy()
        self.input()
        self.getStatus()
        self.move(dt)
        self.checkContact()
        self.animate(dt)
        self.detectFireboltCollision()
        self.mana += dt * 7
        self.health += dt
        if self.mana > 100:
            self.mana = 100
        if self.health > 250:
            self.health = 250
        self.healthBar.health = self.health
        self.manaBar.mana = self.mana
        self.manaBar.rect.midbottom = self.rect.midtop
        self.healthBar.rect.midbottom = self.manaBar.rect.midtop


class Deathbolt(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups, enemies):
        super().__init__(groups)
        self.enemies = enemies
        self.amount = 15
        self.z = assets.LEVELS['level1']['Level']

        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

        # float based movement
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = direction
        self.speed = 400

    def detectEnemyCollision(self):
        for sprite in self.enemies.sprites():
            if self.rect.colliderect(sprite):
                sprite.damage(self.amount)
                self.kill()

    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.rect.y = round(self.pos.y)

    def update(self, dt):
        self.move(dt)
        self.detectEnemyCollision()
    
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, groups, player, manabar):
        super().__init__(groups)
        self.z = assets.LEVELS['level1']['Level']
        self.image = pygame.Surface((2 * player.rect.width, player.rect.height / 4))
        self.rect = self.image.get_rect(midbottom = manabar.rect.midtop)
        self.image.fill('red', (0, 0, self.rect.width, self.rect.height))

        self.health = player.health
        self.maxHealth = self.health
    
    def computeCurrentHealthPercent(self):
        percent = self.health / self.maxHealth
        # print(percent)
        percentRect = pygame.Rect(0, 0, round(self.rect.width * percent), self.rect.height)
        self.image.fill('red', percentRect)
        percentRect = pygame.Rect(round(self.rect.width * percent), 0, self.rect.width - round(self.rect.width * percent), self.rect.height)
        self.image.fill('black', percentRect)


    def update(self, dt):
        self.computeCurrentHealthPercent()


class ManaBar(pygame.sprite.Sprite):
    def __init__(self, groups, player):
        super().__init__(groups)
        self.z = assets.LEVELS['level1']['Level']
        self.image = pygame.Surface((2 * player.rect.width, player.rect.height / 4))
        self.rect = self.image.get_rect(midbottom = player.rect.midtop)
        self.image.fill('blue', (0, 0, self.rect.width, self.rect.height))

        self.mana = player.mana
        self.maxMana = self.mana
    
    def computeCurrentManaPercent(self):
        percent = self.mana / self.maxMana
        # print(percent)
        percentRect = pygame.Rect(0, 0, round(self.rect.width * percent), self.rect.height)
        self.image.fill('blue', percentRect)
        percentRect = pygame.Rect(round(self.rect.width * percent), 0, self.rect.width - round(self.rect.width * percent), self.rect.height)
        self.image.fill('black', percentRect)


    def update(self, dt):
        self.computeCurrentManaPercent()
