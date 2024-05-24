import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0)):
        super().__init__()
        tile1 = pygame.image.load('tile1.png').convert_alpha()
        tile2 = pygame.image.load('tile2.png').convert_alpha()
        self.tiles = [tile1, tile2]
        self.image = self.tiles[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.dragging = False

        # To track rotation value to reapply on flip
        self.rotation = 0
        self.flipped = False

    def drag(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self.dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
            if self.dragging and event.type == pygame.MOUSEMOTION:
                self.rect.move_ip(event.rel)

    def rotate(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.rect.collidepoint(pygame.mouse.get_pos()):
                # Keep the rotation value from growing too much
                self.rotation -= 90
                if self.rotation % 360 == 0: self.rotation = 0
                self.image = pygame.transform.rotate(self.image, -90)

    def flip(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f and self.rect.collidepoint(pygame.mouse.get_pos()):
                self.flipped = not self.flipped
                self.image = self.tiles[self.flipped]
                # Reapply previous rotation
                self.image = pygame.transform.rotate(self.image, self.rotation)

    def update(self, events):
        self.drag(events)
        self.rotate(events)
        self.flip(events)
