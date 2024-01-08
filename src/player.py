import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("../graphics/0.png")
        self.rect = self.image.get_rect(center = pos)
        self.pos = pygame.math.Vector2(pos)
        