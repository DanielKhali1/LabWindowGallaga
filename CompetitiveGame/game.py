import pygame as p
import serial
import time
import threading
import random

class Bullet:

    def __init__(self, posx, posy, speed, direction):
            rect = p.rect.Rect((posx+30, posy, 4, 25))
            self.rect = p.draw.rect(Display, (0, 250, 0), (posx+10, posy, 10, 26))
            self.speed = speed
            self.direction = direction

    def move(self):
        if self.direction:
            self.rect.move_ip(0, -self.speed)
        else:
            self.rect.move_ip(0, self.speed)

    def __del__(self):
        return

class Star:

    def __init__(self, posx, posy, speed):
            rect = p.rect.Rect((random.random()*1000, 0, 4, 25))
            self.rect = p.draw.rect(Display, (255, 255, 255), (random.random()*1000, 0, 5,5))
            self.speed = speed

    def move(self):
        self.rect.move_ip(0, self.speed)

    def __del__(self):
        return




SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720


numBulletsOutAtTime = 20
bulletSpeed = 7
bullets = []
stars = []
maxStars = 40

starSpawnChance = 0.2
starSpeed = 4

gMoveRight = False
gMoveLeft = False

bMoveRight = False
bMoveLeft = False

player1Health = 3
player2Health = 3

moveSpeed = 7

gameOver = False

p.init()
Display = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), p.NOFRAME)
crashed = False

Player1S = p.image.load('BlueShootyBoi.png')
Player1S = p.transform.scale(Player1S, (140, 140))

Player2S = p.image.load('RedShootyBoi.png')
Player2S = p.transform.scale(Player2S, (140, 140))

Player2BS = p.image.load('RedLaser.png')
Player2BS = p.transform.scale(Player2BS, (60, 80))

Player1BS = p.image.load('BlueLaser.png')
Player1BS = p.transform.scale(Player1BS, (60, 80))

Player1HP = p.image.load('BlueHealth.png')
Player1HP = p.transform.scale(Player1HP, (150, 150))

Player2HP = p.image.load('RedHealth.png')
Player2HP = p.transform.scale(Player2HP, (150, 150))

goodGuy = p.rect.Rect((p.display.get_surface().get_size()[0]/2, p.display.get_surface().get_size()[1]/9, 40, 40))
badGuy = p.rect.Rect((p.display.get_surface().get_size()[0]/2, p.display.get_surface().get_size()[1]/1.3, 40, 40))
#p.draw.rect(Display, (0, 0, 0) (200, 200, 25, 25))

#goodGuyHP1 = p.rect.Rect((20, p.display.get_surface().get_size()[1]/11, 30, 30))
#goodGuyHP2 = p.rect.Rect((60, p.display.get_surface().get_size()[1]/11, 30, 30))
#goodGuyHP3 = p.rect.Rect((100, p.display.get_surface().get_size()[1]/11, 30, 30))

goodGuyHP1 = p.rect.Rect((p.display.get_surface().get_size()[0]/12, p.display.get_surface().get_size()[1]/50, 30, 30))
goodGuyHP2 = p.rect.Rect((p.display.get_surface().get_size()[0]/6, p.display.get_surface().get_size()[1]/50, 30, 30))
goodGuyHP3 = p.rect.Rect((p.display.get_surface().get_size()[0]/8, p.display.get_surface().get_size()[1]/50, 30, 30))

largeText = p.font.Font('freesansbold.ttf',30)
bPlayer1 = largeText.render('Player 1', True, (200, 200, 255))

badGuyHP1 = p.rect.Rect((p.display.get_surface().get_size()[0]/12, p.display.get_surface().get_size()[1]/1.1, 30, 30))
badGuyHP2 = p.rect.Rect((p.display.get_surface().get_size()[0]/6, p.display.get_surface().get_size()[1]/1.1, 30, 30))
badGuyHP3 = p.rect.Rect((p.display.get_surface().get_size()[0]/8, p.display.get_surface().get_size()[1]/1.1, 30, 30))

rPlayer2 = largeText.render('Player 2', True, (255, 150, 150))


#game gui
def drawGUI():

    if player1Health >= 3:
        Display.blit(Player1HP, (goodGuyHP1.left-40, goodGuyHP1.top-40))
        #p.draw.rect(Display, (135, 135, 255), goodGuyHP1)
    if player1Health >= 2:
        Display.blit(Player1HP, (goodGuyHP2.left-40, goodGuyHP2.top-40))
        #p.draw.rect(Display, (135, 135, 255), goodGuyHP2)
    if player1Health >= 1:
        Display.blit(Player1HP, (goodGuyHP3.left-40, goodGuyHP3.top-40))
        #p.draw.rect(Display, (135, 135, 255), goodGuyHP3)

    Display.blit(bPlayer1, (p.display.get_surface().get_size()[0]/1.25, p.display.get_surface().get_size()[1]/50))

    if player2Health >= 3:
        Display.blit(Player2HP, (badGuyHP1.left-40, badGuyHP1.top-60))
    #    p.draw.rect(Display, (255, 0, 0), badGuyHP1)
    if player2Health >= 2:
        Display.blit(Player2HP, (badGuyHP2.left-40, badGuyHP2.top-60))
    #    p.draw.rect(Display, (255, 0, 0), badGuyHP2)
    if player2Health >= 1:
        Display.blit(Player2HP, (badGuyHP3.left-40, badGuyHP3.top-60))
    #    p.draw.rect(Display, (255, 0, 0), badGuyHP3)

    Display.blit(rPlayer2, (p.display.get_surface().get_size()[0]/1.25, p.display.get_surface().get_size()[1]/1.1))
# gameover gui

youLost = largeText.render('Player 1 has won!', True, (255, 255, 255))
tryAgain = largeText.render('press any button to Start Over', True, (255, 255 ,255))

def drawGameOverGUI():
    Display.blit(youLost, (p.display.get_surface().get_size()[0]/(2.5), p.display.get_surface().get_size()[1]/3))
    Display.blit(tryAgain, (p.display.get_surface().get_size()[0]/3.2, p.display.get_surface().get_size()[1]/2))




def movePlayer1():
    if(gMoveRight and goodGuy.left < p.display.get_surface().get_size()[0]-40):
        goodGuy.move_ip(moveSpeed, 0)
    elif(gMoveLeft and goodGuy.left > 0):
        goodGuy.move_ip(-moveSpeed, 0)

def movePlayer2():
    if(bMoveRight and badGuy.left < p.display.get_surface().get_size()[0]-40):
        badGuy.move_ip(moveSpeed, 0)
    elif(bMoveLeft and badGuy.left > 0):
        badGuy.move_ip(-moveSpeed, 0)

def shoot(direction):
    #limit the number of bullets out at one time
    if(len(bullets) < numBulletsOutAtTime):
        if(direction):
            bullets.append(Bullet(badGuy.left+14, badGuy.top, bulletSpeed, direction))
        else:
            bullets.append(Bullet(goodGuy.left+14, goodGuy.top, bulletSpeed, direction))

def starSpawn():
    stars.append(Star(random.random()*p.display.get_surface().get_size()[0]-40, 0, starSpeed))


def resetGame():
    global bullets
    global stars
    global player1Health
    global player2Health
    global goodGuy
    global badGuy

    while len(bullets) != 0:
        del bullets[0]

    while len(stars) != 0:
        del stars[0]

    stars = []
    bullets = []
    player1Health = 3
    player2Health = 3

    goodGuy = p.rect.Rect((p.display.get_surface().get_size()[0]/2, p.display.get_surface().get_size()[1]/9, 40, 40))
    badGuy = p.rect.Rect((p.display.get_surface().get_size()[0]/2, p.display.get_surface().get_size()[1]/1.3, 40, 40))
    bMoveLeft = False
    bMoveRight = False
    gMoveLeft = False
    gMoveLeft = False

while not crashed:
    events = p.event.get()

    if not gameOver:

        for event in events:
            if event.type == p.QUIT:
                crashed = True
            if event.type == p.KEYDOWN:
                #if the user presses the A key
                if event.key == p.K_q:
                    # player will start moving left
                    gMoveLeft = True
                    gMoveRight = False
                #if the user presses the D key
                if event.key == p.K_w:
                    # player will start moving right
                    gMoveRight = True
                    gMoveLeft = False
                #if the user presses the Spacebar
                if event.key == p.K_e:
                    # player will shoot
                    shoot(False)

                if event.key == p.K_i:
                    # player will start moving left
                    bMoveLeft = True
                    bMoveRight = False
                #if the user presses the D key
                if event.key == p.K_o:
                    # player will start moving right
                    bMoveRight = True
                    bMoveLeft = False
                #if the user presses the Spacebar
                if event.key == p.K_p:
                    # player will shoot
                    shoot(True)


            if event.type == p.KEYUP:
                #if the player releases the A key
                if event.key == p.K_q:
                    # player will stop moving left
                    gMoveLeft = False
                #if the player releases the D key
                if event.key == p.K_w:
                    # player will stop moving right
                    gMoveRight = False

                if event.key == p.K_i:
                    # player will stop moving left
                    bMoveLeft = False
                #if the player releases the D key
                if event.key == p.K_o:
                    # player will stop moving right
                    bMoveRight = False

        if(starSpawnChance > random.random() and len(stars) < maxStars):
            starSpawn()

        movePlayer1()
        movePlayer2()

        Display.fill((0,0,0))
        for bullet in bullets:
            #move the bullet up
            bullet.move()
            #draw the bullet
            if bullet.direction:
                Display.blit(Player2BS, (bullet.rect.left-25, bullet.rect.top-25))
                #p.draw.rect(Display,(250, 0, 0), bullet.rect)
            else:
                Display.blit(Player1BS, (bullet.rect.left-25, bullet.rect.top-25))
                #p.draw.rect(Display,(135, 135, 255), bullet.rect)

            #if the bullet goes past the top of the screen
            if(bullet.rect.top < 0 or bullet.rect.top > p.display.get_surface().get_size()[1]):
                #remove the bullet from its friends and family
                bullets.remove(bullet)
                #kill the bullet with no witnesses
                del bullet
                #move on and ask no questions
                continue

            if bullet.direction:
                if(bullet.rect.left < goodGuy.left+35 and bullet.rect.left+5 > goodGuy.left and bullet.rect.top < goodGuy.top+35 and bullet.rect.top > goodGuy.top):
                    #subtract from the players health
                    player1Health -= 1
                    #take the bullet out of the list
                    bullets.remove(bullet)
                    #remove the bullet from memory
                    del bullet
                    #go on to the next bullet
                    if player1Health < player2Health and player1Health <= 0:
                        youLost = largeText.render('Player 2 has won!', True, (200, 200, 255))
                        gameOver = True
                        break

                    continue
            else:
                if(bullet.rect.left < badGuy.left+35 and bullet.rect.left+5 > badGuy.left and bullet.rect.top < badGuy.top+35 and bullet.rect.top > badGuy.top):
                    #subtract from the players health
                    player2Health -= 1
                    #take the bullet out of the list
                    bullets.remove(bullet)
                    #remove the bullet from memory
                    del bullet
                    #go on to the next bullet

                    if player2Health < player1Health and player2Health <= 0:
                        youLost = largeText.render('Player 1 has won!', True, (255, 150, 150))
                        gameOver = True
                        break

                    continue




            #for each start in the stars list
        for star in stars:
            #move the star down
            star.move()
            #if the star is off the bottom of the screen
            if(star.rect.top > 800):
                #put it back to the top of the screen
                star.rect.move_ip(0, -820)

            #draw the star on the screen
            p.draw.rect(Display,(255, 255, 255), star.rect)

        drawGUI()

        Display.blit(Player1S, (goodGuy.left-40, goodGuy.top-40))
        #p.draw.rect(Display, (135, 135, 255), goodGuy)
        Display.blit(Player2S, (badGuy.left-40, badGuy.top-40))
        #p.draw.rect(Display, (255, 0, 0), badGuy)
    else:

        for event in events:
            if event.type == p.QUIT:
                crashed = True
            if event.type == p.KEYDOWN:
                resetGame()
                gameOver = False

        Display.fill((0, 0, 0))
        drawGameOverGUI()



    p.display.update()

p.display.quit()
p.quit()
exit()
