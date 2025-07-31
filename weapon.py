import pygame
import random
import constants

class Weapon:
  def __init__(self, weapon_img):
    self.original_img = weapon_img
    self.angle = 0
    self.img = pygame.transform.rotate(self.original_img, self.angle)
    self.rect = self.img.get_rect()
    self.rect.width += 20
    self.used = False
    self.last_used = pygame.time.get_ticks()

  def update(self, player, enemy_list):
    hit_cooldown = 300
    self.rect.center = player.rect.center
    if not player.flip:
      self.rect.x = player.rect.x
    else:
      self.rect.x = player.rect.x - 40

    # reset variables
    damage = 0
    damage_pos = None

    if player.strike and self.used == False and (pygame.time.get_ticks() - self.last_used) >= hit_cooldown:
      for enemy in enemy_list:
        if enemy.rect.colliderect(self.rect) and enemy.alive:
          damage = 10 + random.randint(-5, 5)
          damage_pos = enemy.rect
          enemy.health -= damage
          # enemy.pooked = True
          enemy.hit = True
          self.used = True
          self.last_used = pygame.time.get_ticks()  # reseting the timer
          break
    if not player.attack:
      self.used = False
    return damage, damage_pos

  def draw(self, surface, player):
    flipped_image = pygame.transform.flip(self.original_img, player.flip, False)
    self.img = pygame.transform.rotate(flipped_image, self.angle)
    surface.blit(self.img, ((self.rect.centerx - int(self.img.get_width()/2)), self.rect.centery - int(self.img.get_height()/2)))
    pygame.draw.rect(surface, constants.RED, self.rect, 1)




