import pygame


class SelectBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()

    def resize(self, event, pos=(0, 0)):
        width = 0
        height = 0

        if event.pos[0] >= pos[0]:
            self.rect.x = pos[0]
            width = event.pos[0] - pos[0]
        else:
            self.rect.x = event.pos[0]
            width = pos[0] - event.pos[0]
        if event.pos[1] >= pos[1]:
            self.rect.y = pos[1]
            height = event.pos[1] - pos[1]
        else:
            self.rect.y = event.pos[1]
            height = pos[1] - event.pos[1]

        self.image = pygame.Surface((width, height))
        self.image.fill('grey')

    def get_selected_sprites(self,  sprite_group):
        # Clears the box
        self.image = pygame.Surface((0, 0))

        # Find and return the selected sprites
        print(pygame.sprite.spritecollide(self, sprite_group, False))
        return None
