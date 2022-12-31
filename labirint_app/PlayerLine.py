import pygame

class PlayerLine(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.line = self.image.get_rect()
        self.rect.topleft = (x, y)