import pygame


class SelectBox(pygame.sprite.Sprite):
    def __init__(self, color='grey'):
        super().__init__()
        surface = pygame.Surface((pygame.display.Info().current_w, pygame.display.Info().current_h))
        surface.fill(color)
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.w = 50
        self.rect.h = 50

    def resize(self, event, pos=(0, 0)):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.rect.w += event.rel[0]
        self.rect.h += event.rel[1]
        print('here')
