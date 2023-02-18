from pygame import *
from random import randint
import time as timer


clock = time.Clock()

font.init()
font_1 = font.SysFont("Arial", 27) 
font_2 = font.SysFont("Arial", 300) 
font_3 = font.SysFont("Arial", 50)


window = display.set_mode((700, 500))
display.set_caption("Shooter")

background = transform.scale(image.load("galaxy.jpg"), (700, 500))


class GameSprite(sprite.Sprite):
    def __init__(self, img, x_cor, y_cor, player_speed, scalex=40, scaley=50):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(img), (scalex, scaley))
        self.rect = self.image.get_rect()
        self.rect.x = x_cor
        self.rect.y = y_cor
        self.speed = player_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        
        if (keys[K_a] or keys[K_LEFT]) and self.rect.x > 10:
            self.rect.x -= self.speed
        if (keys[K_d] or keys[K_RIGHT]) and self.rect.x < 635:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx - 1, self.rect.centery, 15, 20 )
        bullets.add(bullet)
        

class Enemy(GameSprite):
    def update(self):
        global missed

        if self.rect.y <= 500:
            self.rect.y += self.speed
        elif self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(10, 650)

            missed += 1
                
class Bullet(GameSprite):
    def update(self):
        if self.rect.y >= -20:
            self.rect.y -= self.speed
        else:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        if self.rect.y <= 500:
            self.rect.y += self.speed
        elif self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(10, 650)

player = Player("spaceship.png", 325, 400, 10, 64, 64)

enemy = Enemy("ufo.png", randint(10, 650), 50, randint(1, 3), 54,54)
enemy1 = Enemy("ufo.png", randint(50, 650), 50, randint(1, 3), 54, 54)
enemy2 = Enemy("ufo.png", randint(50, 650), 50, randint(1, 3), 54, 54)
enemy3 = Enemy("ufo.png", randint(10, 650), 50, randint(1, 3), 54, 54)
enemy4 = Enemy("ufo.png", randint(10, 650), 50, randint(1, 3), 54, 54)

enemys = sprite.Group()
enemys.add((enemy, enemy1, enemy2, enemy3, enemy4))

asteroid_1 = Asteroid("asteroid.png", randint(10, 650), 50, randint(1,2), 54, 54)
asteroid_2 = Asteroid("asteroid.png", randint(10, 650), 50, 1, 54, 54)
asteroid_3 = Asteroid("asteroid.png", randint(10, 650), 50, 3, 54, 54)
asteroid_4 = Asteroid("asteroid.png", randint(10, 650), 50, randint(1,2), 54, 54)

asteroids = sprite.Group()
asteroids.add((asteroid_1, asteroid_2, asteroid_3, asteroid_4))

bullets = sprite.Group()

green = (130, 237, 0)
red = (247, 32, 28)
white = (255, 255, 255)

fps = 60
running = True
finish = False

missed = 0
shooted = 0
player_bullets = 5

refreshingBullets = False
startRefreshTime = None
lengthOfTime = 3

while running:
    
    missed_enemy = font_1.render("Missed: " + str(missed), 1, white)
    shooted_enemy = font_1.render("Shooted: " + str(shooted), 1, white)
    reloading = font_3.render("Reloading pls wait ", 1, white)

    for e in event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN and e.key == K_SPACE:
                if player_bullets > 0:
                    player.fire()
                    player_bullets -= 1
                elif not refreshingBullets:
                    refreshingBullets = True
                    startRefreshTime = timer.time()
        if e.type == K_SPACE and finish == True:
            finish = False


    window.blit(background, (0, 0))
    window.blit(shooted_enemy, (50, 100))
    window.blit(missed_enemy, (50, 50))
    
    if finish == False:
        
        asteroids.draw(window)
        asteroids.update()

        enemys.draw(window)
        enemys.update()

        bullets.draw(window)
        bullets.update()
        
        player.reset()
        player.update()
        
        window.blit(missed_enemy, (50, 50))
        
        if refreshingBullets == True:
            window.blit(reloading, (250, 450))
            time_now = timer.time()
            if time_now - startRefreshTime >= lengthOfTime:
                refreshingBullets = False  
                player_bullets = 5

        for c in sprite.groupcollide(bullets, enemys, True, True):
            shooted += 1
            enemys.add(Enemy("ufo.png", randint(10, 650), 50, randint(1, 3), 54, 54))

        if shooted == 3:
            win = font_2.render("Win", 1, green)
            window.blit(win, (100, 50))
            finish = True

        if missed >= 20 or sprite.spritecollide(player, asteroids, False):
            lose = font_2.render("Lose", 1, red)
            window.blit(lose, (100, 50))
            finish = True
    
    
        display.update()
    clock.tick(fps)