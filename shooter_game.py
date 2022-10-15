#Create your own shooter
from pygame import *
import random

game = True
finish = False
now = 0
reloading = False

#GameSprite class
class GameSprite(sprite.Sprite):
    def __init__(self, player_img, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_img),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()

        #arrowkeys
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= 10
        if keys_pressed[K_RIGHT] and self.rect.x < 625:
            self.rect.x += 10
    
    def fire(self):
        global bullet_counter
        global now
        global reloading
        reloading = False

        if bullet_counter >= 5:
            if time.get_ticks() - now < 3000:
                reloading = True
            else:
                bullet_counter = 0
        else:
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -10, 15, 20)
            bullet_counter += 1
            bullet_group.add(bullet)
            now = time.get_ticks()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > 500:
            global missed_counter
            missed_counter += 1
            self.rect.y = 0
            self.rect.x = random.randint(0,625)

    def respawn(self):
        self.rect.y = 0
        self.rect.x = random.randint(0,625)

class Asteroids(GameSprite):
    def update(self):
        self.rect.y += self.speed
        
        if self.rect.y > 500:
            global asteroid_counter
            self.rect.y = 0
            self.rect.x = random.randint(0,625)

    def respawn(self):
        self.rect.y = 0
        self.rect.x = random.randint(0,625)


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            #print("destroy")
            self.kill()
            del self

#sounds
mixer.init()
mixer.music.load('space.ogg')
#fireSound = mixer.Sound('fire.ogg')
#mixer.music.play()

#FPS
clock = time.Clock()
FPS = 60

#counters
hit_counter = 0
asteroid_counter = 0
missed_counter = 0
bullet_counter = 0

#window
window = display.set_mode((700,500))
display.set_caption('The Shooter Game')
background = transform.scale(image.load("galaxy.jpg"), (700,500))

#fonts
font.init()
font1 = font.SysFont('Comic Sans MS', 23, True)
font2 = font.SysFont('Comic Sans MS', 50, True)
font3 = font.SysFont('Comic Sans MS', 34, True)

#win or lose
win = font2.render('YOU WIN', True, (250, 250, 250))
lose = font2.render('YOU LOSE', True, (250, 250, 250))
asteroid_lifes = font3.render('3 LIVES USED', True, (250,250,250))
two_lives_left = font1.render('2 lives left', True, (250, 250, 250))
one_life_left = font1.render('1 life left', True, (250, 250, 250))
reloading_txt = font1.render('Reloading...', True, (250,250,250))

#creating groups
enemies_group = sprite.Group()
asteroid_group = sprite.Group()
player_group = sprite.Group()
bullet_group = sprite.Group()

#creating player
player = Player("rocket.png", 300, 400, 10, 65, 65)
player_group.add(player)

#creating enemy &  adding to group
for i in range(5):
        enemies_group.add(Enemy("ufo.png", random.randint(0, 625), 10, random.randint(1,3), 65, 65))

#creating asteroid & adding to group
for i in range(3):
        asteroid_group.add(Asteroids("asteroid.png", random.randint(0, 625), 10, random.randint(1,3), 65, 65))

#game loop
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #fireSound.play()
                player.fire()
    

    if hit_counter == 6:
        finish = True
        window.blit(background, (0,0))
        window.blit(win, (150,250))

    if missed_counter >= 8:
        finish = True
        window.blit(background, (0,0))
        window.blit(lose, (150,250))

    if asteroid_counter >= 3:
        finish = True
        window.blit(background, (0,0))
        window.blit(asteroid_lifes, (150,250))


    
    if finish != True:
        collided_sprites = sprite.groupcollide(enemies_group, bullet_group, False, True)
        for item in collided_sprites:
            item.respawn()
            hit_counter += 1

        collided_asteroids = sprite.groupcollide(asteroid_group, player_group, True, False)
        for item in collided_asteroids:
            item.respawn()
            print("collided asteroids")
            asteroid_counter += 1
            print("asteroid counter is: " + str(asteroid_counter))

        window.blit(background, (0,0))
        player.move()
        player.draw()

        text_hit = font1.render("hit : " + str(hit_counter), 1, (255,255,255))
        window.blit(text_hit, (15, 10))
        text_miss = font1.render("missed : " + str(missed_counter), 1, (255,255,255))
        window.blit(text_miss, (15, 50))

        bullet_group.update()
        bullet_group.draw(window)

        player_group.update()
        player_group.draw(window)

        enemies_group.update()
        enemies_group.draw(window)

        asteroid_group.update()
        asteroid_group.draw(window)

        if asteroid_counter == 1:
            window.blit(two_lives_left, (100,15))

        if asteroid_counter == 2:
            window.blit(one_life_left, (100,15))

        if reloading == True:
            window.blit(reloading_txt, (150,250))

    display.update()
    clock.tick(FPS)