import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.bg = pg.image.load('bg.png').convert()
        self.game_over = pg.image.load('game_over.png')
        self.game_end = pg.image.load('victory_screen.png')
        self.game_end = pg.transform.scale(self.game_end, (WIDTH, HEIGHT))
        self.bg = pg.transform.scale(self.bg, (WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.enrage = True


    def new(self):
        # start a new game
        self.text = "Soul Master"
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.projectile = pg.sprite.Group()
        self.extra_hitbox = pg.sprite.Group()
        self.enemy_projectile = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.player = Player(self)
        self.boss = pg.sprite.Group()
        
        #self.greed = Greed(self)
        #self.soul_master = Soul_master(self, 100, 230)
        #self.soul_master = Soul_master(self, 500, 230)
        self.soul_master = Soul_master(self, 0, 0)
        
        self.all_sprites.add(self.player)
        self.player_group.add(self.player)

        self.player.face = 'right'
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()
        

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

        if self.player.hp == 0:
            self.show_go_screen()
            
        else:
            self.soul_master.kill()
            self.soul_master2.kill()
            self.show_end_screen()

        
           

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        if self.soul_master.hp <= 120 and self.enrage:
            self.soul_master2 = Soul_master(self, 0, 0)
            self.enrage = False
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                
        #check if bullet collide with enemy

        bullet_hit = pg.sprite.groupcollide(self.projectile, self.boss, True, False, pg.sprite.collide_mask)
##        for bullet in boss_hits:
##            print(self.boss)
        for hit in bullet_hit:
            self.hurt_sound.play()
            
            self.soul_master.hurt_sound.play()
            self.soul_master.image = self.soul_master.hurt_frame
            self.soul_master.last_update = self.soul_master.now
            self.soul_master.hp -= 10
                
        sabre_hit = pg.sprite.groupcollide(self.extra_hitbox, self.boss, False, False)      
        for hit in sabre_hit:
            if self.player.slashing == 7:
                self.hurt_sound.play()
                
                self.soul_master.hurt_sound.play()
                self.soul_master.image = self.soul_master.hurt_frame
                self.soul_master.last_update = self.soul_master.now
                self.soul_master.hp -= 15

        #enemy_bullet_hit = pg.sprite.spritecollide(self.player, self.enemy_projectile, False)
        enemy_bullet_hit = pg.sprite.groupcollide(self.enemy_projectile, self.player_group, False, False)
        for hit in enemy_bullet_hit:
            if not self.player.invincible and not self.player.rolling:
                self.player.hp -= 1
                self.player.hud[self.player.hp].kill()
                self.player.last_invincible = self.player.now
                self.hurt_sound.play()
                self.player.invincible = True
                
                
        if self.player.hp == 0 or self.soul_master.hp <= 0:
            self.playing = False
                

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP and not self.player.attacking and not self.player.slashing and not self.player.rolling:
                    self.player.jump()
                if event.key == pg.K_z and self.player.attacking == 0 :
                    self.player.attack()
                if event.key == pg.K_x and self.player.attacking == 0:
                    self.player.slash()
                if event.key == pg.K_c and self.player.attacking == 0:
                    self.player.roll()
                    
                    
                    

    def draw(self):
        # Game Loop - draw
        self.screen.blit(self.bg, (0,0))
##        self.all_sprites.draw(self.screen)
        self.screen_blit = self.screen.blit
        for sprite in self.all_sprites:
            # Now blit the sprites at topleft + offset.
            self.screen_blit(sprite.image, sprite.rect.topleft+sprite.offset)
            #pg.draw.rect(self.screen, (250, 30, 0), sprite.rect, 2)
            
        self.draw_text(str(self.text), 30, WHITE, 80, 15)
        # *after* drawing everything, flip the display
       
        pg.draw.rect(self.screen, RED, (20, 40, self.soul_master.hp, 30))
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.blit(self.bg, (0,0))
        self.game_over_sound = pg.mixer.Sound(os.path.join('sfx', "game_over.wav"))
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Z to shoot", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

        self.hurt_sound = pg.mixer.Sound(os.path.join('sfx', "enemy_damage.wav"))

    def show_go_screen(self):
        # game over/continue
        self.screen.blit(self.game_over, (0,0))
        pg.display.flip()
        
        self.game_over_sound.play()
        self.wait_for_key()
        
    def show_end_screen(self):
        # game over/continue
        self.screen.blit(self.game_end, (0,0))
        pg.display.flip()
        self.game_over_sound.play()
        self.wait_for_key()
        

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_z:
                        waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    
pg.quit()
