# Sprite classes for platform game
import pygame as pg
from settings import *
import os
import glob
vec = pg.math.Vector2
OFFSET = 14.5
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.attacking = 0
        self.slashing = 0
        self.rolling = 0
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.load_sound()
        self.image = self.standing_frames[0] 
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.inflate_ip(-140, -25)
        self.offset = vec( -70, -25)
        
        
    def load_sound(self):
        self.shoot_sound = pg.mixer.Sound(os.path.join('sfx', "shoot.wav"))
        self.melee_sound = pg.mixer.Sound(os.path.join('sfx', "melee.wav"))
        self.roll_sound = pg.mixer.Sound(os.path.join('sfx', "roll.wav"))

    def load_images(self):
        self.rect_frame = pg.image.load(os.path.join('idle', 'sub.png'))
        self.standing_frames = [pg.image.load(os.path.join('idle', 'Idle1.png'))]
        for i in range(len(self.standing_frames)):
            self.standing_frames[i] = pg.transform.scale(self.standing_frames[i], (168, 68))
        self.standing_frames_l = []
        self.standing_frames_l.append(pg.transform.flip(self.standing_frames[0], True, False))
         
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        #walk frame
        self.walk_frames_r = [pg.image.load(os.path.join('char1_run', 'running_1.png'))
                             ,pg.image.load(os.path.join('char1_run', 'running_2.png'))
                             ,pg.image.load(os.path.join('char1_run', 'running_3.png'))
                             ,pg.image.load(os.path.join('char1_run', 'running_4.png'))
                             ,pg.image.load(os.path.join('char1_run', 'running_5.png'))
                             ,pg.image.load(os.path.join('char1_run', 'running_6.png'))
                             ,pg.image.load(os.path.join('char1_run', 'running_7.png'))
                             ,pg.image.load(os.path.join('char1_run', 'running_8.png'))]
        for i in range(len(self.walk_frames_r)):
            self.walk_frames_r[i] = pg.transform.scale(self.walk_frames_r[i], (168, 68))
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))

        #jump frame
        self.jump_frames = [pg.image.load(os.path.join('jump', 'jump_1.png')), pg.image.load(os.path.join('jump', 'jump_2.png'))]
        for i in range(len(self.jump_frames)):
            self.jump_frames[i] = pg.transform.scale(self.jump_frames[i], (168, 68))
            
        self.jump_frames_l = []
        for frame in self.jump_frames:
            frame.set_colorkey(BLACK)
            self.jump_frames_l.append(pg.transform.flip(frame, True, False))
            
        #attack frame 41, 38
        self.attack_frames = [pg.image.load(os.path.join('attack1', 'shot10.png'))
                        ,pg.image.load(os.path.join('attack1', 'shot01.png'))
                        ,pg.image.load(os.path.join('attack1', 'shot02.png'))
                        ,pg.image.load(os.path.join('attack1', 'shot03.png'))
                        ,pg.image.load(os.path.join('attack1', 'shot04.png'))
                        ,pg.image.load(os.path.join('attack1', 'shot05.png'))
                        ,pg.image.load(os.path.join('attack1', 'shot06.png'))
                        ,pg.image.load(os.path.join('attack1', 'shot07.png'))
                        ,pg.image.load(os.path.join('attack1', 'shot08.png'))
                        ,pg.image.load(os.path.join('attack1', 'shot09.png'))]
        for i in range(len(self.attack_frames)):
            self.attack_frames[i] = pg.transform.scale(self.attack_frames[i], (168, 68))
        self.attack_frames_l = []
        for frame in self.attack_frames:
            self.attack_frames_l.append(pg.transform.flip(frame, True, False))
        #Melee attack frame
        self.melee_frames = [pg.image.load(os.path.join('melee', 'slash_00.png'))
                              ,pg.image.load(os.path.join('melee', 'slash_00.png'))
                              ,pg.image.load(os.path.join('melee', 'slash_01.png'))
                              ,pg.image.load(os.path.join('melee', 'slash_02.png'))
                              ,pg.image.load(os.path.join('melee', 'slash_03.png'))
                              ,pg.image.load(os.path.join('melee', 'slash_04.png'))
                              ,pg.image.load(os.path.join('melee', 'slash_05.png'))
                              ,pg.image.load(os.path.join('melee', 'slash_06.png'))
                              ,pg.image.load(os.path.join('melee', 'slash_07.png'))
                              ,pg.image.load(os.path.join('melee', 'slash_08.png'))
                              ,pg.image.load(os.path.join('melee', 'slash_09.png'))
                              ,pg.image.load(os.path.join('melee', 'slash_10.png'))
                              ,pg.image.load(os.path.join('melee', 'slash_11.png'))
                              ,pg.image.load(os.path.join('melee', 'slash_12.png'))
                              ,pg.image.load(os.path.join('melee', 'slash_13.png'))
                              ,pg.image.load(os.path.join('melee', 'slash_14.png'))
                              ,pg.image.load(os.path.join('melee', 'slash_15.png'))
                              ,pg.image.load(os.path.join('melee', 'slash_16.png'))]
                              
                        
        
        for i in range(len(self.melee_frames)):
            self.melee_frames[i] = pg.transform.scale(self.melee_frames[i], (168, 68))
        self.melee_frames_l = []
        for frame in self.melee_frames:
            self.melee_frames_l.append(pg.transform.flip(frame, True, False))
        #rolling frame
        self.roll_frames = [pg.image.load(os.path.join('roll', 'roll0.png'))
                            ,pg.image.load(os.path.join('roll', 'roll1.png'))
                            ,pg.image.load(os.path.join('roll', 'roll2.png'))
                            ,pg.image.load(os.path.join('roll', 'roll3.png'))
                            ,pg.image.load(os.path.join('roll', 'roll4.png'))
                            ,pg.image.load(os.path.join('roll', 'roll5.png'))
                            ,pg.image.load(os.path.join('roll', 'roll6.png'))
                            ,pg.image.load(os.path.join('roll', 'roll7.png'))]                     
        
        for i in range(len(self.roll_frames)):
            self.roll_frames[i] = pg.transform.scale(self.roll_frames[i], (168, 68))
        self.roll_frames_l = []
        for frame in self.roll_frames:
            self.roll_frames_l.append(pg.transform.flip(frame, True, False))

    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP
    def attack(self):
        if self.attacking == 0 and self.vel.x == 0 and self.vel.y == 0 and self.slashing == 0 and not self.rolling:
            self.attacking = 10
            self.shoot_sound.play()
    
    def slash(self):
        if self.attacking == 0 and self.vel.x == 0 and self.vel.y == 0 and self.slashing == 0 and not self.rolling:
            self.slashing = 18
            self.melee_sound.play()
            
    def roll(self):
        if self.attacking == 0 and self.vel.x == 0 and self.vel.y == 0 and self.slashing == 0 and not self.rolling:
            self.rolling = 7
            self.roll_sound.play()
            


    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and not self.attacking and not self.slashing:
            self.acc.x = -PLAYER_ACC
            self.face = 'left'
            
        if keys[pg.K_RIGHT] and not self.attacking and not self.slashing:
            self.acc.x = PLAYER_ACC
            self.face = 'right'

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.3:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # Boundary
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0
        self.rect.midbottom = self.pos
        

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        #display walk animation
        if self.vel.y != 0:
            self.jumping = True
        else:
            self.jumping = False
            
        if self.jumping:
            if now - self.last_update > 10:
                self.last_update = now
                if self.face == 'right':
                    if self.vel.y < 0:
                        self.image = self.jump_frames[0]
                    if self.vel.y > 0:
                        self.image = self.jump_frames[1]
                else:
                    if self.vel.y < 0:
                        self.image = self.jump_frames_l[0]
                    if self.vel.y > 0:
                        self.image = self.jump_frames_l[1]
        if self.walking and not self.jumping and not self.attacking and not self.slashing and not self.rolling:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                    
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                    
        if not self.jumping and not self.walking and not self.attacking and not self.slashing and not self.rolling:
            if now - self.last_update > 50:
                if self.face == 'right':
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                    self.image = self.standing_frames[self.current_frame]
                else:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.standing_frames_l)
                    self.image = self.standing_frames_l[self.current_frame]
                    
        if self.attacking:          
            if now - self.last_update > 50:
                if self.face == 'right':
                    self.last_update = now
                    self.current_frame = 10 - self.attacking
                    if self.current_frame == 5:
                        b = Bullet(self.game, self.pos.x, self.pos.y - 40, self.face)
                    self.image = self.attack_frames[self.current_frame]
                    self.attacking -= 1
                    
                    
                elif self.face == 'left':
                    self.last_update = now
                    self.current_frame = 10 - self.attacking
                    if self.current_frame == 5:
                        b = Bullet(self.game, self.pos.x - 50, self.pos.y - 40, self.face)
                    
                    self.image = self.attack_frames_l[self.current_frame]
                    self.attacking -= 1
                    
                    
        if self.slashing:          
            if now - self.last_update > 25:
                if self.face == 'right':
                    self.last_update = now
                    self.current_frame = 18 - self.slashing
                    self.image = self.melee_frames[self.current_frame]
                    self.slashing -= 1
                    
                elif self.face == 'left':
                    self.last_update = now
                    self.current_frame = 18 - self.slashing                   
                    self.image = self.melee_frames_l[self.current_frame]
                    self.slashing -= 1

        if self.rolling:          
            if now - self.last_update > 25:
                if self.face == 'right':
                    self.last_update = now
                    self.current_frame = 7 - self.rolling
                    self.image = self.roll_frames[self.current_frame]
                    self.rolling -= 1
                    
                    self.pos.x += 15
                    
                elif self.face == 'left':
                    self.last_update = now
                    self.current_frame = 7 - self.rolling
                    self.image = self.roll_frames_l[self.current_frame]
                    self.rolling -= 1
                    
                    self.pos.x -= 15
                        
                    
                

class Bullet(pg.sprite.Sprite):
    def __init__(self, game,  x, y, direction):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join('200', 'energy_blast5.png'))
        self.rect = self.image.get_rect()
        self.direction = direction
        self.offset = vec(0,0)
        if direction == 'right':
            self.speed = 10
        else:
            self.speed = -10
        self.rect.x = x
        self.rect.y = y
        
        self.current_frame = 0
        self.last_update = 0
        #load image
        self.frames = [pg.image.load(os.path.join('200', 'energy_blast0.png'))
                       ,pg.image.load(os.path.join('200', 'energy_blast1.png'))
                       ,pg.image.load(os.path.join('200', 'energy_blast2.png'))
                       ,pg.image.load(os.path.join('200', 'energy_blast3.png'))
                       ,pg.image.load(os.path.join('200', 'energy_blast4.png'))
                       ,pg.image.load(os.path.join('200', 'energy_blast5.png'))
                       ,pg.image.load(os.path.join('200', 'energy_blast6.png'))
                       ,pg.image.load(os.path.join('200', 'energy_blast7.png'))]
        self.frames_l = []
        for frame in self.frames:
            self.frames_l.append(pg.transform.flip(frame, True, False))      

    def update(self):
        self.rect.x += self.speed
        now = pg.time.get_ticks()
        if now - self.last_update > 20:
                if self.direction == 'right':
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.frames)
                    self.image = self.frames[self.current_frame]
                else:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.frames_l)
                    self.image = self.frames_l[self.current_frame]
        if self.rect.x > WIDTH or self.rect.x < -50 :
           self.kill()
        

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        self.offset = vec(0,0)
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join('platform', 'platform.png'))
        self.image = pg.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Greed(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join('greed', 'greed0.png'))
        self.offset = vec(0,0)

        self.rect = self.image.get_rect()
        self.direction = 'right'
        self.offset = vec(0,0)
        self.speed = 1
        self.count = 0
        self.rect.x = x
        self.rect.y = y
        
        self.current_frame = 0
        self.last_update = 0

        #load image
        self.frames = [pg.image.load(os.path.join('greed', 'greed0.png'))
                       ,pg.image.load(os.path.join('greed', 'greed1.png'))
                       ,pg.image.load(os.path.join('greed', 'greed2.png'))
                       ,pg.image.load(os.path.join('greed', 'greed3.png'))
                       ,pg.image.load(os.path.join('greed', 'greed4.png'))
                       ,pg.image.load(os.path.join('greed', 'greed5.png'))
                       ,pg.image.load(os.path.join('greed', 'greed6.png'))
                       ,pg.image.load(os.path.join('greed', 'greed7.png'))]
        
        for i in range(len(self.frames)):
            self.frames[i] = pg.transform.scale(self.frames[i], (200, 217))
                      
        self.frames_l = []
        for frame in self.frames:
            self.frames_l.append(pg.transform.flip(frame, True, False))

    def update(self):
        self.rect.x += self.speed
        now = pg.time.get_ticks()
        if now - self.last_update > 200:
                if self.direction == 'right':
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.frames)
                    self.image = self.frames[self.current_frame]
                    self.count += 1
                    if self.count == 8:
                        self.count = 0
                        self.speed = -self.speed
                        self.direction = 'left'
                        print('change')
                    
                else:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.frames_l)
                    self.image = self.frames_l[self.current_frame]
                    self.count += 1
                    if self.count == 8:
                        self.count = 0
                        self.speed = -self.speed
                        self.direction = 'right'
                        print('return')
        if self.rect.x > WIDTH or self.rect.x < -50 :
           self.kill()











        
