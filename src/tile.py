import pygame, assets

class InvisibleWall():
	def __init__(self, x, y, width, height, which):
		self.rect = pygame.Rect(x, y, width, height)
		self.which = which

class Tile(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups, z):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = z
		
class CollisionTile(Tile):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups, assets.LEVELS['level1']['Border'])
		self.oldRect = self.rect.copy()

class MovingObject(CollisionTile):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)

		# float based movement
		self.direction = pygame.math.Vector2(0, -1)
		self.speed = 50
		self.pos = pygame.math.Vector2(self.rect.topleft)
	
	def update(self, dt):
		self.oldRect = self.rect.copy()
		self.pos.y += self.direction.y * self.speed * dt
		self.rect.topleft = (round(self.pos.x), round(self.pos.y))

class Portal(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(groups)
		self.image = surf
		self.image = pygame.transform.scale(self.image, (2 * self.image.get_width(), 2 * self.image.get_height()))
		self.rect = self.image.get_rect(topleft = pos)
		self.z = 3
		