import pygame, assets
from os import walk

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path, player):
        super().__init__(groups)
        self.player = player

        self.importGraphics(path)
        self.frameIndex = 0
        self.status = 'left_stand'
        self.image = self.animations[self.status][self.frameIndex]
        self.rect = self.image.get_rect(topleft = pos)
        self.z = assets.LEVELS['level1']['Level']

        self.detectRange = 600
        self.attackRange = 400
        self.attackPower = 20
        self.health = 100

    def animate(self, dt):
        self.frameIndex += 20 * dt
        if self.frameIndex >= len(self.animations[self.status]):
            self.frameIndex = 0
        self.image = self.animations[self.status][int(self.frameIndex)]

    def importGraphics(self, path):
        self.animations = {}
        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(folder[2], key = lambda str: int(str.split('.')[0])):
                    path = folder[0].replace('\\', '/') + '/' + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    surf = pygame.transform.scale(surf, (assets.width / 8, surf.get_height() * assets.width / (8 * surf.get_width())))
                    key = folder[0].split('\\')[1]
                    self.animations[key].append(surf)
        self.fireboltSurf = pygame.image.load('../graphics/particles/flame/fire/firebolt.png').convert_alpha()
    
    def getPlayerDistanceDirection(self):
        enemy_pos = pygame.math.Vector2(self.rect.center)
        player_pos = pygame.math.Vector2(self.player.rect.center)
        distance = (player_pos - enemy_pos).magnitude()

        if distance != 0:
            direction = (player_pos - enemy_pos).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def detectPlayer(self):
        dist, direction = self.getPlayerDistanceDirection()
        if dist < self.detectRange:
            if -0.5 < direction.y < 0.5:
                if direction.x < 0:
                    self.status = 'left_stand'
                else:
                    self.status = 'right_stand'

    def checkDeath(self):
        if self.health <= 0:
            self.kill()

    def damage(self, amount):
        self.health -= amount

class Imp(Enemy):
    def __init__(self, pos, groups, path, player):
        super().__init__(pos, [groups[0], groups[1]], path, player)

        self.allSprites = groups[0]
        self.fireboltSprites = groups[2]

        self.attacking = False
        self.attackPower = 5
        self.health = 15

        self.lastAttack = 0

    def attackSpell(self):
        distToPlayer = self.getPlayerDistanceDirection()[0]
        if distToPlayer < self.attackRange and not self.attacking:
            self.attacking = True
            self.frameIndex = 0
        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def spellCooldown(self):
        if pygame.time.get_ticks() - self.lastAttack > 1000:
            return True
        return False

    def animate(self, dt):
        if int(self.frameIndex) == 2 and self.attacking and self.spellCooldown():
            if self.getPlayerDistanceDirection()[0] < self.attackRange:
                Firebolt(self.fireboltSurf, self.rect.topleft, self.getPlayerDistanceDirection()[1], [self.allSprites, self.fireboltSprites])
                self.lastAttack = pygame.time.get_ticks()
        self.frameIndex += 7 * dt
        if self.frameIndex >= len(self.animations[self.status]):
            self.frameIndex = 0
            if self.attacking:
                self.attacking = False
        self.image = self.animations[self.status][int(self.frameIndex)]

    def update(self, dt):
        self.detectPlayer()
        self.attackSpell()

        self.animate(dt)
        self.checkDeath()

class Firebolt(pygame.sprite.Sprite):
    def __init__(self, surf,  pos, direction, groups):
        super().__init__(groups)
        self.amount = 3
        self.z = assets.LEVELS['level1']['Level']

        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

        # float based movement
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = direction
        self.speed = 200

    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.rect.y = round(self.pos.y)

    def update(self, dt):
        self.move(dt)




