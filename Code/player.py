import pygame

class Player(): 
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.movespeed = 3

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def move(self):
        # Dictionary of keys pressed with 1 for key pressed, 0 for key not pressed
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            self.x -= self.movespeed
        if keys_pressed[pygame.K_RIGHT]:
            self.x += self.movespeed
        if keys_pressed[pygame.K_UP]:
            self.y -= self.movespeed
        if keys_pressed[pygame.K_DOWN]:
            self.y += self.movespeed
        self.update()