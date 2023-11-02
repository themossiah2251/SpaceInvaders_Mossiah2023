

import pygame, sys

from player import Player
from alien import Alien,Extra
import obstacle
from random import choice, randint
from laser import Laser
from main_menu import MainMenu
class Game:
   #player setup 
   def __init__(self,screen_width,screen_height):
      player_sprite = Player((screen_width/2,screen_height),screen_width,5)
      self.player = pygame.sprite.GroupSingle(player_sprite)
      
  # health/score

      self.lives = 3
      self.live_surf = pygame.image.load('../sprites/player1.png').convert_alpha()
      self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0]* 2+20)
      self.score = 0
      self.font = pygame.font.Font('../font/Daedra.ttf',20)
      
  # obstacle setup
      self.shape = obstacle.shape
      self.block_size = 6
      self.blocks = pygame.sprite.Group()
      self.obstacle_amount = 4
      self.obstacle_x_positions = [num*(screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
      self.create_more_obstacles(*self.obstacle_x_positions, x_start= screen_width / 15, y_start=480)
# alien setup
      self.alien = pygame.sprite.Group()
      self.alien_lasers = pygame.sprite.Group()
      
      self.alien_setup(rows = 6, cols = 8)
      self.alien_direction = 1
# Extra      
      self.extra = pygame.sprite.GroupSingle() 
      self.extra_spawn_time = randint(400,800)
      
# Audio
      music = pygame.mixer.Sound('../music/si.mp3')
      music.set_volume(0.2)
      music.play(loops = -1)

      self.laser_sound = pygame.mixer.Sound('../music/laser4.wav')
      self.laser_sound.set_volume(0.5)      
      self.explosion_sound = pygame.mixer.Sound('../music/explosion.wav')
      self.explosion_sound.set_volume(0.3)
                                 
   def display_main_menu(self):
    font = pygame.font.Font('../font/Daedra.ttf', 60)
    title = font.render("SPACE INVADERS", False, "white")
    title_rect = title.get_rect(center=(screen_width / 2, screen_height / 4))
    screen.blit(title, title_rect)

    start_button_text = font.render("Start Game", False, "white")
    start_button_rect = start_button_text.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(start_button_text, start_button_rect)
    
    return start_button_rect  # returning this rect to check for click event

   def create_obstacle(self,x_start,y_start,offset_x):
      for row_index, row in enumerate(self.shape):
         for col_index,col in enumerate(row):
            if col == 'x':
               x = x_start + col_index * self.block_size + offset_x
               y = y_start + row_index * self.block_size
               block = obstacle.Block(self.block_size,(241,79,175),x,y)
               self.blocks.add(block)
               
   def create_more_obstacles(self,*offsets,x_start, y_start):
    for offset_x in offsets:
        self.create_obstacle(x_start, y_start, offset_x)
        
   def alien_setup(self,rows,cols,x_offset = 70,y_offset = 100,x_distance = 60 ,y_distance = 48):
      for row_index, row in enumerate(range(rows)): #tells what row im on
         for col_index, col in enumerate(range(cols)):
            x = col_index * x_distance + x_offset
            y = row_index * y_distance + y_offset
            
            if row_index == 0: alien_sprite = Alien('yellow',x,y)
            elif 1 <= row_index <= 2: alien_sprite = Alien('green',x,y)
            else: alien_sprite = Alien('red',x,y)
            self.alien.add(alien_sprite)
               
           
            self.alien.add(alien_sprite)
            
   def alien_position_check(self):
       all_aliens = self.alien.sprites()
       for alien in all_aliens:
          if alien.rect.right >= screen_width:
             self.alien_direction = -1
             self.alien_move_down(2)
          elif alien.rect.left <= 0:
             self.alien_direction = 1
             self.alien_move_down(2)
             

   def alien_move_down(self,distance):
      if self.alien:
        for alien in self.alien.sprites():
           alien.rect.y += distance
   
           
   def alien_shoot(self):
      if self.alien.sprites():
       random_alien = choice(self.alien.sprites())  
       laser_sprite = Laser(random_alien.rect.center,6)
       self.alien_lasers.add(laser_sprite)
       self.laser_sound.play()
   def extra_timer(self):
      self.extra_spawn_time -= 1
      if self.extra_spawn_time <= 0:
         self.extra.add(Extra(choice(['right','left']),screen_width))
         self.extra_spawn_time = randint(400,800)
   
   def collistion_checks(self):
      #player lasers
      if self.player.sprite.lasers:
         for laser in self.player.sprite.lasers:
            #obstacle collision
           if pygame.sprite.spritecollide(laser,self.blocks,True):
               laser.kill()
            #alien collision
           alien_hit = pygame.sprite.spritecollide(laser,self.alien,True)
           if alien_hit:
               for alien in alien_hit:
                  self.score += alien.value
               pass
               self.explosion_sound.play()
           #extra
           if pygame.sprite.spritecollide(laser,self.extra,True):
               self.score += 500
               laser.kill()
               
           #alien lasers
      if self.alien_lasers:
         for laser in self.alien_lasers:
            if pygame.sprite.spritecollide(laser,self.blocks,True):
               laser.kill()
            if pygame.sprite.spritecollide(laser,self.player,False):
               laser.kill()
               self.lives -= 1
               if self.lives <= 0: 
                state = GAME_OVER
           #aliens
               
      if self.alien:
         for alien in self.alien:
            pygame.sprite.spritecollide(alien,self.blocks,True)
            
            if pygame.sprite.spritecollide(alien,self.player,False):
               state = GAME_OVER
   def display_lives(self):
      for live in range(self.lives - 1):
         x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0]+10))
         screen.blit(self.live_surf,(x,8))
         

   def display_score(self):
      score_surf = self.font.render(f'score:{self.score}',False,'white')
      score_rect = score_surf.get_rect(topleft = (0,0))
      screen.blit(score_surf,score_rect)
   
   def victory(self):
      if not self.alien.sprites():
         victory_surf = self.font.render('YOU WIN',False,'white')
         victory_rect = victory_surf.get_rect(center = (screen_width / 2,screen_height / 2))
         screen.blit(victory_surf,victory_rect)
         return True
      return False 
   def display_game_over(self,score):
    font = pygame.font.Font('../font/Daedra.ttf', 60)
    title = font.render("GAME OVER", False, "white")
    title_rect = title.get_rect(center=(screen_width / 2, screen_height / 4))
    screen.blit(title, title_rect)

    score_text = font.render(f'Score: {score}', False, "white")
    score_rect = score_text.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(score_text, score_rect)

    retry_button_text = font.render("Retry", False, "white")
    retry_button_rect = retry_button_text.get_rect(center=(screen_width / 2, 3*screen_height / 4))
    screen.blit(retry_button_text, retry_button_rect)

    return retry_button_rect  
   def reset(self):
        self.__init__(screen_width, screen_height)
   def victory_delay(self):
    pygame.time.wait(2000)     
   def run(self):
       # update sprite group
      self.player.update()
      self.alien.update(self.alien_direction)
      self.alien_position_check()
      self.alien_lasers.update()
      self.extra_timer()
      self.extra.update()
      self.collistion_checks()
      
      # draw sprite groups
      self.player.draw(screen)
      self.player.sprite.lasers.draw(screen)
      self.blocks.draw(screen)
      self.alien.draw(screen)
      self.alien_lasers.draw(screen)
      self.extra.draw(screen)
      self.display_lives()
      self.display_score()
      self.victory()


if __name__ == '__main__':
   pygame.init()
   screen_width = 600
   screen_height = 600
   screen = pygame.display.set_mode((screen_width,screen_height))
   clock = pygame.time.Clock()
   game = Game(screen_width,screen_height)
 
   ALIENLASER = pygame.USEREVENT + 1
   pygame.time.set_timer(ALIENLASER,800) #timer set up for alien lasers so they dont shoot all the time
   

   MAIN_MENU, GAME_RUNNING, GAME_OVER = range(3)
   state = MAIN_MENU

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state == MAIN_MENU and event.type == pygame.MOUSEBUTTONDOWN:
            button_rect = game.display_main_menu()  
            if button_rect.collidepoint(event.pos):  
                state = GAME_RUNNING
                game.reset()

        if state == GAME_OVER and event.type == pygame.MOUSEBUTTONDOWN:
            retry_button_rect = game.display_game_over(game.score)  
            if retry_button_rect.collidepoint(event.pos):  
                state = MAIN_MENU

        if state == GAME_RUNNING and event.type == ALIENLASER:
            game.alien_shoot()

    screen.fill((30,30,30))

    if state == MAIN_MENU:
        game.display_main_menu()
    elif state == GAME_RUNNING:
        game.run()
        if game.lives <= 0:
            state = GAME_OVER
        elif game.victory():
            pygame.display.flip()  
            game.victory_delay()  
            game.reset() 
            state = MAIN_MENU
    elif state == GAME_OVER:
        game.display_game_over(game.score)

    pygame.display.flip()
    clock.tick(60)
     
