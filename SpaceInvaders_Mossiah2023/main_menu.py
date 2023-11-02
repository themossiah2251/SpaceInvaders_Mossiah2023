import pygame

class MainMenu:
    def __init__(self,screen_width,screen_height, screen):
        self.screen = screen
        self.font = pygame.font.Font('../font/Daedra.ttf', 40)
        self.title_font = pygame.font.Font('../font/Daedra.ttf', 60)
        self.title = self.title_font.render("SPACE INVADERS", False, "white")
        self.start_button_text = self.font.render("Start Game", False, "white")
        self.title_rect = self.title.get_rect(center=(screen_width / 2, screen_height / 4))
        self.start_button_rect = self.start_button_text.get_rect(center=(screen_width / 2, screen_height / 2))

    def display(self):
        self.screen.blit(self.title, self.title_rect)
        self.screen.blit(self.start_button_text, self.start_button_rect)

    def check_click(self, pos):
        return self.start_button_rect.collidepoint(pos)



