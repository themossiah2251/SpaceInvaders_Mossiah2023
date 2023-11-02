import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self,colour,x,y):
        super().__init__()
        file_path = '../sprites/'+ colour +'.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,y))

        if colour == 'red': self.value = 100
        elif colour == 'green': self.value = 200
        else: self.value = 300

    def update(self,direction):
        self.rect.x += direction
         
class Extra(pygame.sprite.Sprite):
    def __init__(self,side,screen_width):
        super().__init__()
        self.image = pygame.image.load('../sprites/extra.png').convert_alpha()
        if side == 'right':
            x = screen_width + 50
            self.speed = -3 
        else:
            x = 50
            self.speed = 3
            
        self.rect = self.image.get_rect(topleft = (x,80))
        
    def update(self):
        self.rect.x += self.speed


