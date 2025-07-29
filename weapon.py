import pygame
import random

class Weapon:
  def __init__(self, player):
    self.rect = player.rect
    #self.rect.update()
    self.used = False
    self.last_used = pygame.time.get_ticks()

  def update(self, player, enemy_list):
    hit_cooldown = 300
    # reset variables
    damage = 0
    damage_pos = None
    if player.attack and self.used == False and (pygame.time.get_ticks() - self.last_used) >= hit_cooldown:
      for enemy in enemy_list:
        if enemy.rect.colliderect(self.rect) and enemy.alive:
          damage = 10 + random.randint(-5, 5)
          damage_pos = enemy.rect
          enemy.health -= damage
          enemy.pooked = True
          # enemy.hurt = True
          enemy.hit = True
          self.used = True
          self.last_used = pygame.time.get_ticks()  # reseting the timer
          break
    if not player.attack:
      self.used = False
    return damage, damage_pos




