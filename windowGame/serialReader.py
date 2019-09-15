import serial
import pygame
import random

pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('windowBoi')
clock = pygame.time.Clock()

crashed = False

rect = pygame.rect.Rect((400, 525, 25, 25))
pygame.draw.rect(gameDisplay, (0, 200, 0), (64, 54, 18, 18))

scoreVal = 0

largeText = pygame.font.Font('freesansbold.ttf',30)
score = largeText.render('Score: 0', True, (255, 255, 255))

heartImg = pygame.image.load('heart.png')
heartImg = pygame.transform.scale(heartImg, (60, 60))


currentAction = 0
#ser = serial.Serial('/dev/tty.usbserial-A5027LAV')
#ser.flushInput()

moveLeft = False
moveRight = False

bulletSpeed = 15
starSpeed = 20
enemyBulletSpeed = 5

enemySpawnChance = 0.01

textrect = score.get_rect()
textrect.move_ip(550, 30)

class Bullet:

    def __init__(self, posx, posy, speed):
            rect = pygame.rect.Rect((posx+10, posy, 4, 25))
            self.rect = pygame.draw.rect(gameDisplay, (0, 250, 0), (posx+10, posy, 4, 25))
            self.speed = speed

    def move(self):
        self.rect.move_ip(0, -self.speed)

    def __del__(self):
        return


class Star:

    def __init__(self, posx, posy, speed):
            rect = pygame.rect.Rect((random.random()*800, 0, 4, 25))
            self.rect = pygame.draw.rect(gameDisplay, (255, 255, 255), (random.random()*800, 0, 5,5))
            self.speed = speed

    def move(self):
        self.rect.move_ip(0, self.speed)

    def __del__(self):
        return

class Enemy:
    def __init__(self, posx, posy, furthestYposition):
            rect = pygame.rect.Rect((random.random()*800, 0, 25, 25))
            self.rect = pygame.draw.rect(gameDisplay, (255, 0, 0), (random.random()*800, 0, 25,25))
            self.shootChance = 0.01
            self.furthestYposition = furthestYposition

            self.right = ((int)(random.random() + 0.5) > 0) if False else True

    def step(self):
        if(self.rect.top < self.furthestYposition):
            self.rect.move_ip(0, 4)
        else:
            if(self.shootChance >= random.random()):
                enemybullets.append(EnemyBullet(self.rect.left, self.rect.top, enemyBulletSpeed))
            if(self.right):
                self.rect.move_ip(3, 0)
                if(self.rect.left > 775):
                    self.right = False
            else:
                self.rect.move_ip(-3, 0)
                if(self.rect.left < 25):
                    self.right = True

    def __del__(self):
        return


class EnemyBullet:

    def __init__(self, posx, posy, speed):
            rect = pygame.rect.Rect((posx+10, posy, 4, 25))
            self.rect = pygame.draw.rect(gameDisplay, (0, 250, 0), (posx+10, posy, 4, 25))
            self.speed = speed

    def move(self):
        self.rect.move_ip(0, self.speed)

    def __del__(self):
        return


enemybullets = []
bullets = []
stars = []
enemies = []


def shoot():
    bullets.append(Bullet(rect.left, rect.top, bulletSpeed))

def starSpawn():
    stars.append(Star(random.random()*800, 0, starSpeed))

def enemySpawn():
    enemies.append(Enemy(random.random()*700+50, 0, random.random()*100 + 100))


while not crashed:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
                crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moveLeft = True
            if event.key == pygame.K_d:
                moveRight = True
            if event.key == pygame.K_SPACE:
                shoot()


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moveLeft = False
            if event.key == pygame.K_d:
                moveRight = False

    if(0.3 > random.random() and len(stars) < 10):
        starSpawn()



    if(moveLeft and rect.left > 0):
        rect.move_ip(-7, 0)
    elif(moveRight and rect.left < 775):
        rect.move_ip(7, 0)



    gameDisplay.fill((0, 0, 0))


    if(enemySpawnChance >= random.random() and len(enemies) < 20):
        enemySpawn()


    for bullet in bullets:
        bullet.move()
        pygame.draw.rect(gameDisplay,(0, 250, 0), bullet.rect)

        if(bullet.rect.top < 0):
            bullets.remove(bullet)
            del bullet
            continue

    for eBullet in enemybullets:
        eBullet.move()
        pygame.draw.rect(gameDisplay,(255, 0, 0), eBullet.rect)
        if(eBullet.rect.top > 600):
            enemybullets.remove(eBullet)
            del eBullet
            continue

    for enemy in enemies:
        continued = False
        for bullet in bullets:
            if(bullet.rect.left < enemy.rect.left+35 and bullet.rect.left+5 > enemy.rect.left and bullet.rect.top < enemy.rect.top+35 and bullet.rect.top > enemy.rect.top):
                scoreVal += 10
                score = largeText.render('Score: '+str(scoreVal), True, (255, 255, 255))
                enemies.remove(enemy)
                del enemy
                continued = True
                break

        if(continued):
            continue

        enemy.step()
        pygame.draw.rect(gameDisplay,(255, 0, 0), enemy.rect)


    for star in stars:
        star.move()
        if(star.rect.top > 600):
            star.rect.move_ip(0, -620)
            #stars.remove(star)
            #del star
            #break

        pygame.draw.rect(gameDisplay,(255, 255, 255), star.rect)

    gameDisplay.blit(score, textrect)

    gameDisplay.blit(heartImg, (30, 15))
    gameDisplay.blit(heartImg, (70, 15))
    gameDisplay.blit(heartImg, (110, 15))



    pygame.draw.rect(gameDisplay, (0, 200, 0), rect)
    ##try:
    ##    ser_bytes = ser.readline()
    ##    decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
##
##        if decoded_bytes == 3:
##            rect.move_ip(-5, 0)
##        elif decoded_bytes == 8:
##            rect.move_ip(5, 0)
##        else:
##            rect.move_ip(0, 0)
##
##        print(decoded_bytes)
##    except:
##        print("Keyboard Interrupt")
##        break

    pygame.display.update()

    clock.tick(40)

pygame.display.quit()
pygame.quit()
exit()
