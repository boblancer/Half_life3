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
        self.bg = pg.transform.scale(self.bg, (WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

    def new(self):
        # start a new game
        self.boss = "Next boss : Ultra Greed"
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.bullet = pg.sprite.Group()
        self.player = Player(self)
        self.greed = Greed(self, 100, 230)
        self.enemy = pg.sprite.Group()
        self.all_sprites.add(self.player)
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

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

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
            
        self.draw_text(str(self.boss), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.blit(self.bg, (0,0))
        self.start_sound = pg.mixer.Sound(os.path.join('sfx', "unicorn.wav"))
        self.start_sound.play()
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Z to shoot", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str('jack'), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()

##    def show_go_screen(self):
##        # game over/continue
##        if not self.running:
##            return
##        self.screen.fill(BGCOLOR)
##        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
##        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
##        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
##
##    
##        pg.display.flip()
##        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
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
    g.show_go_screen()

pg.quit()
