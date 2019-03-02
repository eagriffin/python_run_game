import pygame
from random import randint
from vec2d import vec2d
import time
from factorfinder import factorfinder

class runner(pygame.sprite.Sprite):
    def __init__(self, screen, initpos, position=[0,0], image = 'starter.png'):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.pos = vec2d(initpos)
        self.basepos = initpos
        self.rect = self.image.get_rect().move(self.pos.x,self.pos.y)
        self.screen = screen
        self.position = position
        self.change = 0
        self.acting = False
        self.invinc = False
    def update(self, speed):
        types = ['starter.png', 'fullstride.png', 'midstride.png',\
                 'lowstride.png', 'jump.png', 'slide.png', 'invisible.png']
        # regular
        if self.change == 0:
            if self.position[1] == 0 or self.position == [3,2]:
                self.position = [2,1]
            elif self.position[1] == 3:
                self.position = [3,2]
            elif self.position == [1,2]:
                self.position = [2,3]
            elif self.position[1] == 1:
                self.position = [1,2]
            self.image = pygame.image.load(types[self.position[-1]])
            if self.position[1] == 2:
                self.change = 2
            else:
                self.change = 4
        # jump
        if self.change > 90 and self.change < 105:
            self.pos.y -= 9
            self.rect = self.image.get_rect().move(self.pos.x,self.pos.y)
            self.change -= 1
        if self.change > 40 and self.change < 51:
            self.pos.y += 9
            self.rect = self.image.get_rect().move(self.pos.x, self.pos.y)
            self.change -= 1
        if self.change == 40:
            self.land()
        # slide
        if self.change > 190 and self.change <= 200:
            self.pos.y += 3
            self.rect = self.image.get_rect().move(self.pos.x,self.pos.y)
            self.change -= 1
        if self.change > 140 and self.change < 143:
            self.pos.y -= 15
            self.rect = self.image.get_rect().move(self.pos.x, self.pos.y)
            color = self.image.get_at((0,0))
            self.image.set_colorkey(color)
            self.change -= 1
        if self.change == 140:
            self.land()
        # invincible
        if self.change > 210 and self.change < 300 and self.change%2 == 0:
            if self.position[1] == 1:
                self.position = [1, 6]
            elif self.position[1] == 3:
                self.position = [3, 6]
            elif self.position[1] == 2:
                self.position = [self.position[0]+2, 6]
            elif self.position[0] == 12:
                self.position = [6, 3]
            elif self.position[0] == 32:
                self.position = [6,1]
            elif self.position[0] == 1:
                self.position = [10,2]
            elif self.position[0] == 3:
                self.position = [30,2]
            self.image = pygame.image.load(types[self.position[-1]])
            self.change -= 1
        if self.change > 200 and self.change <= 210:
            self.change = 0
            self.position = [2,1]
            self.invinc = False
        else:
            self.change -= 1

    def jump(self):
        self.image = pygame.image.load('jump.png')
        color = self.image.get_at((0,0))
        self.pos = vec2d(self.basepos)
        self.rect = self.image.get_rect().move(self.pos.x, self.pos.y)
        self.image.set_colorkey(color)
        self.change = 100
        self.position = [0,4]
        self.acting = 'jump'
        self.invinc = False
    def land(self):
        self.change = 1
        self.image = pygame.image.load('fullstride.png')
        self.position = [2,1]
        self.acting = False
    def slide(self):
        self.change = 200
        self.image = pygame.image.load('slide.png')
        self.pos = vec2d(self.basepos)
        self.rect = self.image.get_rect().move(self.pos.x, self.pos.y)
        color = self.image.get_at((0,0))
        self.image.set_colorkey(color)
        self.position = [0,5]
        self.acting = 'slide'
        self.invinc = False
    def invincible(self):
        self.invinc = True
        self.change = 300
        if self.position[1] == 4 or self.position[1] == 5:
            self.pos = vec2d(self.basepos)
            self.rect = self.image.get_rect().move(self.pos.x, self.pos.y)
        self.position = [2,1]
        
        
class Block(pygame.sprite.Sprite):
    def __init__(self, initpos, screen, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('brkwall.png')
        self.pos = vec2d(initpos)
        self.rect = self.image.get_rect().move(self.pos.x,self.pos.y)
        self.screen = screen
        self.speed = speed
    def update(self, speed):
        self.speed = speed
        self.pos.x -= self.speed
        self.rect = self.image.get_rect().move(self.pos.x,self.pos.y)

def stext(score, screen):
    font = pygame.font.Font(None, 30)
    sctext = font.render('Score:'+str(score), 1, (255,0,0))
    screen.blit(sctext, (450,0))

def faster(screen):
    font = pygame.font.Font(None, 30)
    ftext = font.render('Faster!', 1, (255,255,0))
    screen.blit(ftext, (230, 100))

class lifetoken(pygame.sprite.Sprite):
    def __init__(self, initpos, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('lifetoken.png')
        self.pos = vec2d(initpos)
        self.screen = screen
        self.rect = self.image.get_rect().move(self.pos.x,self.pos.y)

def rungame():
    pygame.init()

    screen = pygame.display.set_mode((550,250))

    clock = pygame.time.Clock()

    bg1 = pygame.image.load('scrbkgd.png')
    bg2 = pygame.image.load('scrbkgd.png')
    bg1x = 0
    bg2x = bg1.get_width()
    bgfactors = factorfinder(bg1.get_width())

    screen.blit(bg1, (bg1x, 0))
    screen.blit(bg2, (bg2x, 0))

    i = 1
    speed = bgfactors[i]   # possible speeds: 1,2,4,5,8,10,20,25, 

    player = runner(screen, (40,209))
    allsprites = pygame.sprite.Group()
    allsprites.add(player)
    allsprites.draw(screen)

    lives = pygame.sprite.Group()
    life = lifetoken((0, 0), screen)
    life2 = lifetoken((12, 0), screen)
    life3 = lifetoken((24, 0), screen)
    lives.add(life, life2, life3)
    lifes = [life, life2, life3]

    heights = [197, 183, 160]
    block = Block( (550,heights[0]), screen, speed)
    blocks = pygame.sprite.Group()
    blocks.add(block)
    allsprites.add(block)
    pygame.display.flip()

    loops = 0
    ploops = 0
    pause = False
    score = 0
    stext(score,screen)
    while True:
        clock.tick(40)
        
        screen.blit(bg1, (bg1x, 0))
        screen.blit(bg2, (bg2x, 0))
        
        bg1x -= speed
        bg2x -= speed

        if bg1x == -1 * bg1.get_width():
            bg1x = bg2x + bg2.get_width()
        if bg2x == -1 * bg2.get_width():
            bg2x = bg1x + bg1.get_width()
            
        loops += 1
        if loops >= randint(50,110):
            h = randint(0,2)
            block = Block( (550, heights[h]), screen, speed)
            blocks.add(block)
            allsprites.add(block)
            loops = 0
            score += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if player.acting != 'slides':
                    player.slide()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if player.acting != 'jumps':
                    player.jump()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pause = True

            while pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return exit_game()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        pause = False
                        time_passed = clock.tick(40)
                        time_passed = clock.tick(40)
        collision = []
        if not player.invinc:
            collision = pygame.sprite.spritecollide(player, blocks, True)
        if len(collision):
            if len(lives) == 0:
                lose_text(screen)
                allsprites.draw(screen)
                pygame.display.flip()
                gameover(screen)
            else:
                llen = len(lives) - 1
                lives.remove(lifes[llen])
                time_passed = clock.tick(40)
                time_passed = clock.tick(40)
                player.invincible()
        if score == 5:
            i += 1
            speed = 2
            faster(screen)
        allsprites.update(speed)
        allsprites.draw(screen)
        lives.draw(screen)
        stext(score,screen)
        pygame.display.flip()


def exit_game():
    pygame.quit()
    return None

def lose_text(screen):
    font = pygame.font.Font(None, 30)
    ftext = font.render('Game Over!', 1, (255,255,0))
    screen.blit(ftext, (230, 100))

def gameover(screen):
    time.sleep(2)
    pygame.quit()

rungame()
