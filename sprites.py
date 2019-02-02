# Sprite classes for platform game
import pygame as pg
from settings import *
import os
import glob
from random import *
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
        self.invincible = False
        self.last_invincible = 0
        self.hp = 3
        self.face = 'right'
        self.sabre_hitbox = Extra_hitbox(self.game, self, 40, 40, -45, 30 )#(self, game ,root, width, height, off_r, off_l)
        self.hud = [Heart_Hud(self.game, WIDTH - 60 * 3, 10)
                    ,Heart_Hud(self.game, WIDTH - 60 * 2, 10)
                    ,Heart_Hud(self.game, WIDTH - 60 * 1, 10)]
        
        
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
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits:
            self.vel.y = -PLAYER_JUMP
    def attack(self):
        if self.attacking == 0  and self.vel.y == 0 and self.slashing == 0 and not self.rolling:
            self.vel.x = 0
            self.attacking = 10
            self.shoot_sound.play()
    
    def slash(self):
        if self.attacking == 0  and self.vel.y == 0 and self.slashing == 0 and not self.rolling:
            self.vel.x = 0
            self.slashing = 18
            self.melee_sound.play()
            
    def roll(self):
        if self.attacking == 0 and self.slashing == 0 and not self.rolling:
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
        self.now = pg.time.get_ticks()
        if self.now - self.last_invincible > 1000 and self.invincible:
            self.invincible = False

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
            if self.now - self.last_update > 10:
                self.last_update = self.now
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
            if self.now - self.last_update > 100:
                self.last_update = self.now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                    
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                    
        if not self.jumping and not self.walking and not self.attacking and not self.slashing and not self.rolling:
            if self.now - self.last_update > 50:
                if self.face == 'right':
                    self.last_update = self.now
                    self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                    self.image = self.standing_frames[self.current_frame]
                else:
                    self.last_update = self.now
                    self.current_frame = (self.current_frame + 1) % len(self.standing_frames_l)
                    self.image = self.standing_frames_l[self.current_frame]
                    
        if self.attacking:          
            if self.now - self.last_update > 50:
                if self.face == 'right':
                    self.last_update = self.now
                    self.current_frame = 10 - self.attacking
                    if self.current_frame == 5:
                        b = Bullet(self.game, self.pos.x + 20, self.pos.y - 40, self.face)
                    self.image = self.attack_frames[self.current_frame]
                    self.attacking -= 1
                    
                    
                elif self.face == 'left':
                    self.last_update = self.now
                    self.current_frame = 10 - self.attacking
                    if self.current_frame == 5:
                        b = Bullet(self.game, self.pos.x - 50, self.pos.y - 40, self.face)
                    
                    self.image = self.attack_frames_l[self.current_frame]
                    self.attacking -= 1
                    
                    
        if self.slashing:          
            if self.now - self.last_update > 25:
                if self.face == 'right':
                    self.last_update = self.now
                    self.current_frame = 18 - self.slashing
                    self.image = self.melee_frames[self.current_frame]
                    self.slashing -= 1
                    
                elif self.face == 'left':
                    self.last_update = self.now
                    self.current_frame = 18 - self.slashing                   
                    self.image = self.melee_frames_l[self.current_frame]
                    self.slashing -= 1

        if self.rolling:          
            if self.now - self.last_update > 25:
                if self.face == 'right':
                    self.last_update = self.now
                    self.current_frame = 7 - self.rolling
                    self.image = self.roll_frames[self.current_frame]
                    self.rolling -= 1
                    
                    self.pos.x += 10
                    
                elif self.face == 'left':
                    self.last_update = self.now
                    self.current_frame = 7 - self.rolling
                    self.image = self.roll_frames_l[self.current_frame]
                    self.rolling -= 1
                    
                    self.pos.x -= 10
    
        self.mask = pg.mask.from_surface(self.image)
                        
class Projectile(pg.sprite.Sprite):
    def __init__(self, game,  x, y, direction = 'right'):
        self.direction = direction
        self.offset = vec(0,0)
        self.load_image()
        self.current_frame = 0
        self.last_update = 0

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def load_image(self):
        pass
    
class Soul_projectile(Projectile):
    def __init__(self, game,  x, y, speedx, speedy):
        super().__init__(game,  x, y)
        self.groups = game.all_sprites, game.enemy_projectile
        pg.sprite.Sprite.__init__(self, self.groups)
        self.speedx = speedx
        self.speedy = speedy
    
        
    def load_image(self):
        self.image = pg.image.load(os.path.join('Siphon_soul', 'soul_projectile.png'))   
        self.image = pg.transform.scale(self.image , (50, 50))
                                                  
    def update(self):
            
        self.rect.x += self.speedx
        self.rect.y -= self.speedy 
        self.now = pg.time.get_ticks()
        
        if self.rect.x > WIDTH or self.rect.x < -50 or self.rect.y > HEIGHT or self.rect.y < -50:
           self.kill()

                
class Bullet(Projectile):
    def __init__(self, game,  x, y, direction):
        super().__init__(game,  x, y, direction)
        self.groups = game.all_sprites, game.projectile
        pg.sprite.Sprite.__init__(self, self.groups)
        
    def load_image(self):
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
        self.image = self.frames[5]

    def update(self):
        if self.direction == 'right':
            self.speed = 10
        else:
            self.speed = -10
            
        self.rect.x += self.speed
        self.now = pg.time.get_ticks()
        if self.now - self.last_update > 20:
                if self.direction == 'right':
                    self.last_update = self.now
                    self.current_frame = (self.current_frame + 1) % len(self.frames)
                    self.image = self.frames[self.current_frame]
                else:
                    self.last_update = self.now
                    self.current_frame = (self.current_frame + 1) % len(self.frames_l)
                    self.image = self.frames_l[self.current_frame]
        if self.rect.x > WIDTH or self.rect.x < -50 :
           self.kill()
           
        self.mask = pg.mask.from_surface(self.image)
        
class Shockwave(Projectile):
    def __init__(self, game,  x, y, direction):
        super().__init__(game,  x, y, direction)
        self.groups =  game.enemy_projectile, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.last_update = pg.time.get_ticks()

        for frame in self.frames:
            self.frames_l.append(pg.transform.flip(frame, True, False))
        
    def load_image(self):
        
        self.frames = [pg.image.load(os.path.join('shockwave', 'shockwave0.png')),
                       pg.image.load(os.path.join('shockwave', 'shockwave1.png')),
                       pg.image.load(os.path.join('shockwave', 'shockwave2.png'))]
        self.frames_l = []
        for frame in self.frames:
            frame = pg.transform.scale(frame, (119, 140))
        for frame in self.frames:
            self.frames_l.append(pg.transform.flip(frame, True, False))
        self.image = self.frames[0]
        
        
    def update(self):
        self.now = pg.time.get_ticks()
        if self.direction == 'right':
            self.speed = 8
            self.image = self.frames[0]
            if self.now - self.last_update > 250:
                self.image = self.frames[1]
            if self.now - self.last_update > 500:
                self.image = self.frames[2]
        else:
            self.speed = -8
            self.image = self.frames_l[0]
            if self.now - self.last_update > 250:
                self.image = self.frames_l[1]
            if self.now - self.last_update > 500:
                self.image = self.frames_l[2]
            self.mask = pg.mask.from_surface(self.image)
                
        if self.now - self.last_update > 550:
             self.kill()
        self.rect.x += self.speed
        

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
    def __init__(self, game):
        self.groups = game.all_sprites, game.boss
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join('greed', 'greed0.png'))
        self.offset = vec(0,0)

        self.rect = self.image.get_rect()
        self.direction = 'right'
        self.offset = vec(0,0)
        self.speed = 1
        self.count = 0
        self.rect.x = 20
        self.rect.y = 20
        
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
        #sound
        self.hurt_sound = pg.mixer.Sound(os.path.join('sfx', "greed_hurt.wav"))

    def update(self):
        self.rect.x += self.speed
        self.now = pg.time.get_ticks()
        if self.now - self.last_update > 200:
                if self.direction == 'right':
                    self.last_update = self.now
                    self.current_frame = (self.current_frame + 1) % len(self.frames)
                    self.image = self.frames[self.current_frame]
                    self.count += 1
                    if self.count == 8:
                        self.count = 0
                        self.speed = -self.speed
                        self.direction = 'left'
                        
                    
                else:
                    self.last_update = self.now
                    self.current_frame = (self.current_frame + 1) % len(self.frames_l)
                    self.image = self.frames_l[self.current_frame]
                    self.count += 1
                    if self.count == 8:
                        self.count = 0
                        self.speed = -self.speed
                        self.direction = 'right'
                        
        if self.rect.x > WIDTH or self.rect.x < -50 :
           self.kill()
           
class Soul_master(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.boss
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(os.path.join('soul_master', 'soul_idle.png'))
        self.game = game
        self.rect = self.image.get_rect()
        self.direction = 'right'
        self.speed = 0
        self.count = 0
        self.rect.x = x
        self.rect.y = y   
        self.rect.inflate_ip(-170, -170)
        self.offset = vec( -30, -25)
        self.hp = 300
        
        #moves variable
        self.dive = 0
        self.attack = 0
        self.cooldown = 0
        self.roll_dice = 0
        self.predive = [5,6,7]
        self.vanish = [10]
        
        self.current_frame = 0
        self.last_update = 0
        self.load_image()


        #sound
        self.hurt_sound = pg.mixer.Sound(os.path.join('SM_sfx', "Soul_Master_Hurt.wav"))
        self.attack_sounds = [pg.mixer.Sound(os.path.join('SM_sfx', "Soul_Master_Angry_01.wav"))
                            
                              ,pg.mixer.Sound(os.path.join('SM_sfx', "Soul_Master_Angry_03.wav"))
                              
                              ,pg.mixer.Sound(os.path.join('SM_sfx', "Soul_Master_Angry_07.wav"))]
                    
        
##        for i in range(len(self.teleport_frames)):
##            self.frames[i] = pg.transform.scale(self.teleport_frames[i], (300, 300))
                      
    def load_image(self):
        TRANSFORM = 250
        
        self.frames_l = [pg.image.load(os.path.join('soul_master', 'soul_idle.png'))
                       ,pg.image.load(os.path.join('soul_master', 'soul_idle2.png'))]
        
        for i in range(len(self.frames_l)):
            self.frames_l[i] = pg.transform.scale(self.frames_l[i], (TRANSFORM, TRANSFORM))
        
        self.frames = []
        for frame in self.frames_l:
            self.frames.append(pg.transform.flip(frame, True, False))
        
        self.teleport_frames = [pg.image.load(os.path.join('soul_master', 'teleport.png'))
                       ,pg.image.load(os.path.join('soul_master', 'teleport2.png'))]
        
        for i in range(len(self.teleport_frames)):
            self.teleport_frames[i] = pg.transform.scale(self.teleport_frames[i], (TRANSFORM, TRANSFORM))
            
        self.teleport_frames_l = []   
        for frame in self.teleport_frames:
            self.teleport_frames_l.append(pg.transform.flip(frame, True, False))
        
        self.predive_frames = [pg.image.load(os.path.join('soul_master', 'predive.png'))
                       ,pg.image.load(os.path.join('soul_master', 'predive2.png'))]

        self.diving_frames = pg.image.load(os.path.join('soul_master', 'soul_dive.png'))
        self.diving_frames = pg.transform.scale(self.diving_frames, (TRANSFORM, TRANSFORM))
        
        for i in range(len(self.predive_frames)):
            self.predive_frames[i] = pg.transform.scale(self.predive_frames[i], (TRANSFORM, TRANSFORM))

        self.invisible = pg.image.load(os.path.join('soul_master', 'invisible.png'))

        self.hurt_frame_l = pg.image.load(os.path.join('soul_master', 'soul_hurt.png'))
        self.hurt_frame_l = pg.transform.scale(self.hurt_frame_l, (TRANSFORM, TRANSFORM))
        self.hurt_frame = pg.transform.flip(self.hurt_frame_l, True, False)
        
    def update(self):
        self.rect.x += self.speed
        self.now = pg.time.get_ticks()
        self.roll_dice = randint(1, 15)
        if self.roll_dice == 5 and not self.dive and not self.cooldown and not self.attack:
            self.dive = 11
        if self.roll_dice in [1,3] and not self.dive and not self.cooldown and not self.attack:
            self.attack = 6
            
        if self.now - self.last_update > 250 and not self.dive and not self.attack:
                if self.direction == 'right':
                    self.last_update = self.now
                    self.current_frame = (self.current_frame + 1) % len(self.frames)
                    self.image = self.frames[self.current_frame]
                else:
                    self.last_update = self.now
                    self.current_frame = (self.current_frame + 1) % len(self.frames_l)
                    self.image = self.frames_l[self.current_frame]

        if self.dive:
            self.dive_attack()
        if self.attack > 0:
            if self.now - self.last_update > 400:
                if self.attack == 2:
                    Soul_projectile(self.game,  self.rect.x + 80, self.rect.y+ 120, 8, 8)
                    Soul_projectile(self.game,  self.rect.x + 80, self.rect.y+ 120, -8, 8)
                    Soul_projectile(self.game,  self.rect.x + 80, self.rect.y+ 120, 8, -8)
                    Soul_projectile(self.game,  self.rect.x + 80, self.rect.y+ 120, -8, -8)
                    
                if self.attack == 5:
                    Soul_projectile(self.game,  self.rect.x + 80, self.rect.y + 120, -10, 0)
                    Soul_projectile(self.game,  self.rect.x + 80, self.rect.y+ 120,  0, 10)
                    Soul_projectile(self.game,  self.rect.x + 80, self.rect.y+ 120, 0, -10)
                    Soul_projectile(self.game,  self.rect.x + 80, self.rect.y+ 120, 10, 0)
                self.image = self.teleport_frames_l[1]
                self.attack_sounds[randint(0, 2)].play()
                self.attack -= 1
            
                
        self.mask = pg.mask.from_surface(self.image)
                
                
                
        if self.cooldown > 0:
            self.cooldown -= 1
    def dive_attack(self):

        if self.now - self.last_update > 100:
            if self.dive == 12:
                self.last_update = self.now
                self.image = self.teleport_frames_l[0]
                self.dive -= 1
                
            elif self.dive == 11:
                self.last_update = self.now
                self.image = self.teleport_frames_l[1]
                self.dive -= 1
                self.attack_sounds[randint(0, 2)].play()
                
                
            elif self.dive in self.vanish:
                if self.dive == 10:
                    self.rect.x = (self.game.player.pos.x - 160) + randint(-150, 150)
                    self.rect.y = -30
                self.last_update = self.now
                self.image = self.invisible
                self.dive -= 1

                    
            elif self.dive == 9:
                self.last_update = self.now
                self.image = self.teleport_frames_l[1]
                self.dive -= 1
                
            elif self.dive == 8:
                self.last_update = self.now
                self.image = self.teleport_frames_l[0]
                self.dive -= 1
            
            elif self.dive in self.predive:
                self.last_update = self.now
                self.current_frame = (self.current_frame + 1) % len(self.predive_frames)
                self.image = self.predive_frames[self.current_frame]
                self.dive -= 1
                
            elif self.dive == 1:
                warp_spot = [100, 750]
                self.rect.x = warp_spot[randint(0,1)]
                self.rect.y = 100
                self.image = self.teleport_frames_l[1]
                self.dive -= 1
                self.cooldown = 150
                
            else:
                if self.dive == 2:
                    Shockwave( self.game,  self.rect.x , self.rect.y, 'right')
                    Shockwave( self.game,  self.rect.x , self.rect.y, 'left')
                self.last_update = self.now
                self.image = self.diving_frames
                self.dive -= 1
                self.rect.y += 200
        
    
class Extra_hitbox(pg.sprite.Sprite):
    def __init__(self, game ,root, width, height, off_r, off_l):
        self.groups = game.all_sprites, game.extra_hitbox
        pg.sprite.Sprite.__init__(self, self.groups)
        self.offset = vec(0,0)
        self.rect = pg.Rect(root.rect.x, root.rect.y, width, height)
        self.root = root
        self.rect_offset_left = off_r
        self.rect_offset_right = off_l
        self.image = pg.image.load("empty_pixel.png")
        
    def update(self):
        if self.root.face == 'right':
            self.rect.x = self.root.rect.x + self.rect_offset_right
            self.rect.y = self.root.rect.y
        else:
            self.rect.x = self.root.rect.x + self.rect_offset_left
            self.rect.y = self.root.rect.y
    
class Heart_Hud(pg.sprite.Sprite):
    def __init__(self,game, x, y,):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.offset = vec(0,0)
        self.image = pg.image.load("heart.png")
        self.image = pg.transform.scale(self.image , (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
      

    
                
                
            
           
    
        
            
        
        
        











        
