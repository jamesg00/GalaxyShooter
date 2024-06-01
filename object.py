import pygame


screen = pygame.display.set_mode((300, 500))

class Background():
    def __init__(self, win):
        self.win = win
        #image
        self.image = pygame.image.load("assets/j7ldjnurlto91.png")
        self.image = pygame.transform.scale(self.image, (300,500))
        self.rect = self.image.get_rect()
        self.reset()
        self.move = True

    def update(self, speed):
        if self.move:
            self.y1 += speed
            self.y2 += speed
            
            if self.y1 >= 500:
                self.y1 = -500
            if self.y2 >= 500:
                self.y2 = -500

        self.win.blit(self.image, (self.x,self.y1))
        self.win.blit(self.image, (self.x,self.y2))
            
    def reset(self):
        self.x = 0
        self.y1 = 0
        self.y2 = -500
