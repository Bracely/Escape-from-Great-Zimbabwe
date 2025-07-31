import pygame
import math
import constants


class Character:
    def __init__(self, x, y, health, mob_animations, char_type, dangerous = False):
        self.char_type = char_type
        self.score = 0
        self.flip = False
        self.animation_list = mob_animations[char_type]
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:run 2:attack 3:hurt 4:dying
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.health = health
        self.alive = True
        self.hit = False
        self.last_hit = pygame.time.get_ticks()
        self.strike = False
        self.dangerous = dangerous

        # self.wait = 0

        #james'variables
        self.pace_direction = 1
        self.pace_duration = 1000
        self.pace_timer = pygame.time.get_ticks()
        self.pacing_paused = False
        self.pacing_pause_timer = 0
        self.pacing_pause_duration = 1000
        self.pacing = False

        self.stunned = False
        self.hurt = False
        self.attack = False
        self.pooked = False
        self.animation_done = False

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)

    def move(self, dx, dy):
        self.running = False

        if dx != 0 or dy != 0:
            self.running = True
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False
        # control diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)

        self.rect.x += dx
        self.rect.y += dy

    def ai(self, player):
        clipped_line = ()
        stun_cooldown = 400
        ai_dx = 0
        ai_dy = 0

        #create a line of sight from the enemy to the player
        line_of_sight = ((self.rect.centerx, self.rect.centery), (player.rect.centerx, player.rect.centery))

        # # check if line of sight passes through an obstacle tile
        # for obstacle in obstacle_tiles:
        #     if obstacle[1].clipline(line_of_sight):
        #         clipped_line = obstacle[1].clipline(line_of_sight)

        #check distance to player
        dist = math.sqrt(((self.rect.centerx - player.rect.centerx)**2) + ((self.rect.centery - player.rect.centery)**2))

        if self.dangerous and self.pooked == True:
            if not clipped_line and dist > constants.RANGE:
                if self.rect.centerx > player.rect.centerx:
                    ai_dx = -constants.ENEMY_SPEED
                if self.rect.centerx < player.rect.centerx:
                    ai_dx = constants.ENEMY_SPEED
                if self.rect.centery > player.rect.centery:
                    ai_dy = -constants.ENEMY_SPEED
                if self.rect.centery < player.rect.centery:
                    ai_dy = constants.ENEMY_SPEED

        else:
            if not clipped_line and dist < constants.DEER_NOTICE_RANGE - 50:
                if self.rect.centerx > player.rect.centerx:
                    ai_dx = constants.ENEMY_SPEED
                if self.rect.centerx < player.rect.centerx:
                    ai_dx = -constants.ENEMY_SPEED
                if self.rect.centery > player.rect.centery:
                    ai_dy = constants.ENEMY_SPEED
                if self.rect.centery < player.rect.centery:
                    ai_dy = -constants.ENEMY_SPEED

        if self.alive:
            if not self.stunned:

                # pacing
                # if dist > constants.DEER_NOTICE_RANGE:
                #     self.pacing = True
                #     self.move(self.pace_direction * constants.ENEMY_PACE, 0)
                #     if pygame.time.get_ticks() - self.pace_timer > self.pace_duration:
                #         self.pace_direction *= -1
                #         self.pace_timer = pygame.time.get_ticks()
            # running away
            # away from player
                if dist < constants.DEER_NOTICE_RANGE and not self.dangerous:  # use this to make the boar run away
                    self.move(ai_dx, ai_dy)
                # away from player
                elif dist < constants.DEER_NOTICE_RANGE and self.dangerous and not self.pooked:  # use this to make the boar run away
                    constants.ENEMY_SPEED = 2
                    self.move(ai_dx, ai_dy)
            #move towards player
                elif player.health > 0 and self.pooked and self.dangerous: #use this to make the boar run away
                    constants.ENEMY_SPEED = 4
                    self.move(ai_dx, ai_dy)
                    if self.health <= 20:
                        self.pooked = False
                #attack player
                    if dist < constants.ATTACK_RANGE and player.hit == False and not self.hurt  and self.hit == False:
                        player.health -= 10
                        player.hurt = True
                        player.hit = True
                        self.attack = True
                        player.last_hit = pygame.time.get_ticks()
                if  player.health == 0:
                    self.attack = False
                    self.running = False

            #check if hit
            hit_cooldown = 1000
            if self.hit:
                #push back attackers chete
                if self.dangerous and self.health >= 20:
                    if self.rect.centerx - player.rect.centerx > 0:
                        self.rect.x += 25  # only for dangerous enemies
                    else:
                        self.rect.x -= 25
                    self.pooked = True
                self.hit = False
                self.last_hit = pygame.time.get_ticks()
                self.stunned = True
                self.running = False
                self.attack = False ### supposed to cancel the animal

                self.hurt = True
                self.update_action(3)

        if (pygame.time.get_ticks() - self.last_hit > stun_cooldown):
            self.stunned = False
            self.hurt = False
        return self.alive

    def update(self):
        # check if character has died
        if self.health <= 0:
            self.health = 0
            self.attack = False
            self.alive = False

        #timer to reset player taking a hit
        hit_cooldown = 1000
        if self.char_type == 0:
            if self.hit == True and pygame.time.get_ticks() - self.last_hit >hit_cooldown:
                self.hit = False
                self.hurt = False

        # check what action the player is performing
        if self.running:
            self.update_action(1)  # 1:run
        elif self.attack:
            self.update_action(2)  # 2:attack
        elif self.hurt:
            self.update_action(3)  # 3:hurt
        elif not self.alive:
            self.update_action(4)  # 4:dying
        else:
            self.update_action(0)  # 0:idle

        animation_cooldown = 70
        if self.action == 4:
            animation_cooldown = 200
        elif self.action == 2 and self.char_type == 0:
            animation_cooldown = 70

        # handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            if self.action == 4 or self.action == 3 and self.frame_index == 3: #whats the purpose of action==3 here?? its to make the attack frame stop at the last frame is displayed
                self.frame_index = 3
                self.update_time = pygame.time.get_ticks()
            else:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
                if self.action == 2 and self.frame_index == 3:
                    self.strike = True
                    self.attack = False
        # check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            self.strike = False
        # if self.wait == 5:
        #     self.animation_done = True
        # return self.animation_done

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface, constants.RED, self.rect, 1)