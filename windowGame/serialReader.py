import serial
import pygame
import random
import threading


pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('windowBoi')
clock = pygame.time.Clock()
currentAction = 0
#ser = serial.Serial('/dev/tty.usbmodem14101')
#ser.flushInput()

move = 0

bulletSpeed = 15
starSpeed = 20
enemyBulletSpeed = 5

health = 3




crashed = False


spaceShip = pygame.image.load('SpaceShip.png')
spaceShip = pygame.transform.scale(spaceShip, (50, 50))

rect = pygame.rect.Rect((400, 525, 25, 25))
pygame.draw.rect(gameDisplay, (0, 0, 0), (64, 54, 18, 18))

scoreVal = 0


heartImg = pygame.image.load('heart.png')
heartImg = pygame.transform.scale(heartImg, (60, 60))

badGuy = pygame.image.load('badGuy.png')
badGuy = pygame.transform.scale(badGuy, (40, 40))


moveLeft = False
moveRight = False


enemySpawnChance = 0.03

scoreText = pygame.font.Font('freesansbold.ttf', 20)
killedEnemy = scoreText.render('+10', True, (255, 247, 0))


largeText = pygame.font.Font('freesansbold.ttf',30)
score = largeText.render('Score: 0', True, (255, 255, 255))
textrect = score.get_rect()
textrect.move_ip(550, 30)

#print "3"



def takeInput():

    global move
    try:
        #ser_bytes = ser.readline()
        #decoded_bytes = int(ser_bytes[1])
        #print(decoded_bytes)
        decoded_bytes = int(random.random()*4)

        if decoded_bytes == 1:
            move += 1
        elif decoded_bytes == 3:
            move += 3
        elif decoded_bytes == 2:
            move += 2
        else:
            move += 0
    except:
        move += 0

    #print("I'm working")
    #print(move)

class Bullet:

    def __init__(self, posx, posy, speed):
            rect = pygame.rect.Rect((posx+30, posy, 4, 25))
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
points = []


def shoot():
    bullets.append(Bullet(rect.left+14, rect.top, bulletSpeed))

def starSpawn():
    stars.append(Star(random.random()*800, 0, starSpeed))

def enemySpawn():
    enemies.append(Enemy(random.random()*700+50, 0, random.random()*100 + 100))








crashed = False
while not crashed:
    events = pygame.event.get()

    #print("Not Moving")

    #decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    #decoded_bytes = 0
    #decoded_bytes = None


    #print(ser_bytes[1])



    #print("Moving")
    move = 0
    #print(move)
    t1 = threading.Thread(target=takeInput, args=())
    t1.start()
    t1.join()
    #print(move)



    if(move == 1 and rect.left > 0):
        rect.move_ip(-7, 0)
    elif(move == 2 ):
        shoot()
    elif(move == 3 and rect.left < 775):
        rect.move_ip(7,0)



    for event in events:
        if event.type == pygame.QUIT:
                t1.kill()
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

        if(eBullet.rect.left < rect.left+35 and eBullet.rect.left+5 > rect.left and eBullet.rect.top < rect.top+35 and eBullet.rect.top > rect.top):
            #hurt player

            health -= 1

            enemybullets.remove(eBullet)
            del eBullet
            continue

    for enemy in enemies:
        continued = False
        for bullet in bullets:
            if(bullet.rect.left < enemy.rect.left+35 and bullet.rect.left+5 > enemy.rect.left and bullet.rect.top < enemy.rect.top+35 and bullet.rect.top > enemy.rect.top):
                temprect = killedEnemy.get_rect().move(enemy.rect.left, enemy.rect.top)
                points.append(temprect)
                bullets.remove(bullet)
                del bullet
                scoreVal += 10
                score = largeText.render('Score: '+str(scoreVal), True, (255, 255, 255))
                enemies.remove(enemy)
                del enemy
                continued = True
                break
        if(continued):
            continue

        enemy.step()
        gameDisplay.blit(badGuy, (enemy.rect.left, enemy.rect.top))

        #pygame.draw.rect(gameDisplay,(0, 0, 0), enemy.rect)

    for point in points:
        #move up
        point.move_ip(0, -3)
        gameDisplay.blit(killedEnemy, point)
        #if too high kill
        if(point.top < 0):
            points.remove(point)
            del point
            continue



    for star in stars:
        star.move()
        if(star.rect.top > 600):
            star.rect.move_ip(0, -620)
            #stars.remove(star)
            #del star
            #break

        pygame.draw.rect(gameDisplay,(255, 255, 255), star.rect)

    gameDisplay.blit(score, textrect)

    if health > 0:
        gameDisplay.blit(heartImg, (30, 15))
    else:
        crashed = True
        print("Player Died")
    if health > 1:
        gameDisplay.blit(heartImg, (70, 15))
    if health > 2:
        gameDisplay.blit(heartImg, (110, 15))



    pygame.draw.rect(gameDisplay, (0, 0, 0), rect)
    gameDisplay.blit(spaceShip, (rect.left, rect.top))



    pygame.display.update()

    clock.tick(40)

pygame.display.quit()
pygame.quit()
exit()
t1.kill()


#print "1"
#t2 = threading.Thread(target=gameLoop, args=())
#print "2"
#t2.start()
