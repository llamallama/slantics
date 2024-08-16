import pygame


class SelectBox(pygame.sprite.Sprite):
    '''
    Draws the click and drag multi select box
    Extends pygame.Sprite.

    Attributes
    ----------
    image : pygame.Surface
        The current image surface applied to the tile
    rect: int
        The size of the board cells in pixels
    pos : tuple
        The anchor position to draw the select box around

    Methods
    -------
    resize(event):
        Resizes the select box.
    '''
    def __init__(self, pos=(0, 0)):
        super().__init__()
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        self.pos = pos

    def resize(self, event):
        width = 0
        height = 0

        if event.pos[0] >= self.pos[0]:
            self.rect.x = self.pos[0]
            width = event.pos[0] - self.pos[0]
        else:
            self.rect.x = event.pos[0]
            width = self.pos[0] - event.pos[0]
        if event.pos[1] >= self.pos[1]:
            self.rect.y = self.pos[1]
            height = event.pos[1] - self.pos[1]
        else:
            self.rect.y = event.pos[1]
            height = self.pos[1] - event.pos[1]

        self.rect.w = width
        self.rect.h = height
        self.image = pygame.Surface((width, height))
        self.image.fill('grey')
