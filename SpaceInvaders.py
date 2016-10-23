import pygame
from pygame.locals import *
from random import randint

RED = (255, 0, 0)
BLUE = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width = 50, height = 10):
        super().__init__()
    
        self.deltax = 0
        self.deltay = 0
        self.blockWidth = 5
        self.imageA = [
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 0, 1, 0, 1]
        ]

        self.image = pygame.Surface([len(self.imageA[0]) * self.blockWidth, len(self.imageA) * self.blockWidth])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 100


    def update(self):
        self.rect.x += self.deltax
        self.rect.y += self.deltay

        #add collision code

    def update_keydown(self, keycode):
        if keycode.key == pygame.K_a:
            self.deltax = -5
        if keycode.key == pygame.K_d:
            self.deltax = 5
        

    def update_keyup(self, keycode):
        if keycode.key == pygame.K_a:
            self.deltax = 0
        if keycode.key == pygame.K_d:
            self.deltax = 0

    def draw(self, display):
        for x in range(len(self.imageA)):
            for y in range(len(self.imageA[0])):
                if self.imageA[x][y] == 1:
                    pygame.draw.rect(display, (255, 255, 255), (self.rect.x + y * self.blockWidth, self.rect.y + x* self.blockWidth, self.blockWidth, self.blockWidth))
        
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.deltax = 0
        self.dir = 2
        self.deltay = 0
        self.blockWidth = 5
        self.numberEnemies = 0
        
        self.imageA = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 0, 1, 1],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1]
        ]
        self.numberEnemies = 0

        self.image = pygame.Surface([len(self.imageA[0]) * self.blockWidth, len(self.imageA) * self.blockWidth])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1

    def update(self):
        self.bullet_collide = pygame.sprite.spritecollide(self, self.bullet, False)



        for col in self.bullet_collide:
            
            self.kill()
            
            


        if self.dir == 1:
            self.rect.x += self.speed
        if self.dir == 2:
            self.rect.x -= self.speed
    def draw(self, display):
        for x in range(len(self.imageA)):
            for y in range(len(self.imageA[0])):
                if self.imageA[x][y] == 1:
                    pygame.draw.rect(display, (WHITE), (self.rect.x + y * self.blockWidth, self.rect.y + x * self.blockWidth, self.blockWidth, self.blockWidth))
    def set_enemies(self, num):
        self.numberEnemies = num
    def get_enemies(self):
        return self.numberEnemies

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width = 5, height = 5, dir = 1):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.deltay = 10
        self.dir = dir

        if self.dir == 1:
            self.deltay = 10
        else:
            self.deltay = -10
        
    def update(self):
        self.rect.y -= self.deltay


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width = 1, height = 3):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.deltay = 5


    def update(self):
        self.selfcollide = pygame.sprite.spritecollide(self, self.player, False)
        self.rect.y += self.deltay

        for col in self.selfcollide:
            col.health -= 10
            print("you were hit")


    







        
display = pygame.display.set_mode([640, 485])

player_sprite_list = pygame.sprite.Group()
enemy_sprite_list = pygame.sprite.Group()
bullet_sprite_group = pygame.sprite.Group()
enemy_bullet_sprite_group = pygame.sprite.Group()
isRunning = True
clock = pygame.time.Clock()
player = Player(10, 450)

player_sprite_list.add(player)
enemy_list = [
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0]
]

local = 0
for x in range(len(enemy_list)):
    for y in range(len(enemy_list[0])):
        if enemy_list[x][y] == 1:
            enemy = Enemy(y * 75, x * 75)
            enemy.bullet = bullet_sprite_group
            enemy_sprite_list.add(enemy)
            enemy.numberEnemies += 1
print(local)


def draw_planet(x, y, r, c, display):
    pygame.draw.circle(display, (c), (x, y), r, 1) 
    

planetX = 100
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.x + 10, player.rect.y, 2, 4)
                bullet_sprite_group.add(bullet) 
            player.update_keydown(event)


        if event.type == pygame.KEYUP:
            player.update_keyup(event)


        for bullet in bullet_sprite_group:
            if bullet.rect.y < -10:
                bullet_sprite_group.remove(bullet)
            
                
    display.fill(BLACK)
    player_sprite_list.update()
    enemy_sprite_list.update()
    bullet_sprite_group.update()
    enemy_bullet_sprite_group.update()

    #enemy_sprite_list.draw(display)
    #player_sprite_list.draw(display)
    pygame.draw.rect(display, (RED), (randint(10, 640), randint( 10, 480), 2, 2))
    
    bullet_sprite_group.draw(display)
    for enemy in enemy_sprite_list:

        randomnum = randint(0, 1000)

        if randomnum < 500 and randomnum > 490:
            bullet = EnemyBullet(enemy.rect.x, enemy.rect.y, 2, 3)
            enemy_bullet_sprite_group.add(bullet)
            bullet.player = player_sprite_list
            bullet.update()





        
        if enemy.rect.left <= 0:
            
            
            for enemy in enemy_sprite_list:
                
                enemy.imageA = [
                    [1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 1],
                    [1, 1, 0, 1, 1],
                    [0, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0],
                    [0, 1, 0, 1, 0],
                    [1, 0, 1, 0, 1]
                ]
                enemy.dir = 1
                enemy.rect.y += 2
                bullet = EnemyBullet(enemy.rect.x, enemy.rect.y, 10, 10)
                enemy_bullet_sprite_group.add(bullet)
                bullet.player = player_sprite_list
                bullet.update()







                
        if enemy.rect.right > 640:
            for enemy in enemy_sprite_list:
                
                enemy.imageA = [
                    [1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 1],
                    [1, 1, 0, 1, 1],
                    [0, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0],
                    [0, 1, 0, 1, 0],
                    [0, 1, 0, 1, 0]
                ]
                enemy.dir = 2
                enemy.rect.y += 2
                bullet = EnemyBullet(enemy.rect.x, enemy.rect.y, 10, 10)
                enemy_bullet_sprite_group.add(bullet)
                bullet.player = player_sprite_list
                bullet.update()
        print(player.health)
            
        enemy.draw(display)



      
    
    player.draw(display)
    enemy_bullet_sprite_group.draw(display)

    pygame.display.update()
    clock.tick(60)
pygame.quit()

