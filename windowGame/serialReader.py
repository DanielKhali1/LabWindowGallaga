import serial
import pygame
import random
import threading


# delay shooting


## PYGAME SET UP ##
pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('GALLAGA CLONE')
clock = pygame.time.Clock()

#SETS UP SERIAL INPUT /CHANGE PER USB PORT
ser = serial.Serial('/dev/tty.usbserial-A5027LAV')
ser.flushInput()


# PLAYER RECT OBJECT
rect = pygame.rect.Rect((400, 525, 25, 25))
pygame.draw.rect(gameDisplay, (0, 0, 0), (64, 54, 18, 18))



#------------__GAME ATTRIBUTES__-------------#
#IMPORTANT dont change these vaulues
currentAction = 0
highScoreVal = 0
move = 0
health = 3
scoreVal = 0
#change these variables to desired gameplay
numBulletsOutAtTime = 5
bulletSpeed = 15
starSpeed = 20
enemyBulletSpeed = 5
enemySpawnChance = 0.01
starSpawnChance = 0.3

#------------__________________-------------#



#------------__IMG_OBJECTS__-------------#
heartImg = pygame.image.load('heart.png')
heartImg = pygame.transform.scale(heartImg, (60, 60))

badGuy = pygame.image.load('badGuy.png')
badGuy = pygame.transform.scale(badGuy, (40, 40))
spaceShip = pygame.image.load('SpaceShip.png')
spaceShip = pygame.transform.scale(spaceShip, (50, 50))
#------------______________-------------#


#------------__TEXT_OBJECTS__-------------#
scoreText = pygame.font.Font('freesansbold.ttf', 20)
killedEnemy = scoreText.render('+10', True, (255, 247, 0))
hurtText = pygame.font.Font('freesansbold.ttf', 25)
wasHurtTextRender = scoreText.render('- <3', True, (255, 0, 0))
largeText = pygame.font.Font('freesansbold.ttf',30)
medText = pygame.font.Font('freesansbold.ttf',24)
highScore = medText.render('High Score: '+ str(highScoreVal), True, (255, 255, 255))
youLost = largeText.render('YOU LOST', True, (255, 255, 255))
tryAgain = largeText.render('press any button to Start Over', True, (255, 255 ,255))
score = largeText.render('Score: 0', True, (255, 255, 255))
textrect = score.get_rect()

textrect.move_ip(550, 30)
#------------_________________-------------#


#------------__BOOLS__-------------#
dead = False
moveLeft = False
moveRight = False
global crashed
crashed = False
#------------_________-------------#

#------------__LISTS CONTAINING GAME OBJECTS__-------------#
enemybullets = []
bullets = []
stars = []
enemies = []
points = []
hurtText = []
#------------_________-------------#



#--------------------------------------------- OBJECTS -----------------------------------------------#

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
#--------------------------------------------------------------------------------------------------------#


#--- SERIAL INPUT THREAD FUNCTION ---#
def takeInput():

    #grabbing the global variable move
    global move
    #grabbing the global variable crashed
    #global crashed

    #while the game is still playing
    while not crashed:

        try:
            #read serial input in
            ser_bytes = ser.readline()
            print ser_bytes
            #weird ser input so just taking the 2nd character from the serial input line
            decoded_bytes = int(ser_bytes)

            #if serial input = 1 then move = 1
            if decoded_bytes == 3:
                move = 1
            #if serial input = 3 then move = 3
            elif decoded_bytes == 8:
                move = 3
            #if serial input = 2 then move = 2
            elif decoded_bytes == 5 or decoded_bytes == 4 or decoded_bytes == 6 or decoded_bytes == 3:
                move = 2
            #else move = 0
            else:
                move = 0
        except:
            #if every thing breaks move = 0
            move = 0
#------------------------------------------#



#--------------------------------------------- METHODS ----------------------------#

# spawns a bullet at players position
# adds bullet to bullet list
def shoot():
    #limit the number of bullets out at one time
    if(len(bullets) < numBulletsOutAtTime):
        bullets.append(Bullet(rect.left+14, rect.top, bulletSpeed))

#spawns a star in a random x position at the top of the screen
#adds star to the star list
def starSpawn():
    stars.append(Star(random.random()*800, 0, starSpeed))


#spawns an enemy in a random x position at the top of the screen
#adds the enemy to the enemies list
def enemySpawn():
    enemies.append(Enemy(random.random()*700+50, 0, random.random()*100 + 100))
#--------------------------------------------------------------------------------------#

# starting a thread that takes input from the serial port
t1 = threading.Thread(target=takeInput, args=())
t1.start()


#--------------------------------------- GAME LOOP -----------------------------------------------#
while not crashed:
    # will grab all of the current active events that pygame has detected
    # need this to check for inputs, and quiting from the program
    events = pygame.event.get()

    # actual Gameplay loop will run if the player is not dead
    if(not dead):

        # distinguishing move as a global variable
        global move

        # reads the move that the thread has been updating
        # if serial thread reads input from the controller it will update the integer move
        #   1: moves the player 7 pixels to the left
        #   2: will shoot a bullet from the players
        #   3: moves the player 7 pixels to the right

#--------------------------------------- Player Control -----------------------------------------------#


        #if the move is equal to 1 and the player is not outside of the screen
        if(move == 1 and rect.left > 0):
            # moves the player 7 pixels to the left
            rect.move_ip(-7, 0)
            move = 0
        #if the move is equal to 2
        elif(move == 2 ):
            #shoot a bullet
            shoot()
            move = 0
        #if the move is equal to 3 and the player is not outside of the screen
        elif(move == 3 and rect.left < 775):
            # moves the player 7 pixels to the right
            rect.move_ip(7,0)
            move = 0


        #runs through each active event in the list of events per frame
        for event in events:
            # if the user exits the program
            if event.type == pygame.QUIT:
                    crashed = True
            #if the user (using a keyboard) pushes any key down
            if event.type == pygame.KEYDOWN:
                #if the user presses the A key
                if event.key == pygame.K_a:
                    # player will start moving left
                    moveLeft = True
                #if the user presses the D key
                if event.key == pygame.K_d:
                    # player will start moving right
                    moveRight = True
                #if the user presses the Spacebar
                if event.key == pygame.K_SPACE:
                    # player will shoot
                    shoot()
            # once the player releases the key they pressed before
            if event.type == pygame.KEYUP:
                #if the player releases the A key
                if event.key == pygame.K_a:
                    # player will stop moving left
                    moveLeft = False
                #if the player releases the D key
                if event.key == pygame.K_d:
                    # player will stop moving right
                    moveRight = False
        #if the move Left boolean is True and the player is not outside of the screen
        if(moveLeft and rect.left > 0):
            # the player will move 7 pixels to the left of the screen
            rect.move_ip(-7, 0)
        #if the move Right boolean is True and the player is not outside of the screen
        elif(moveRight and rect.left < 775):
            # the player will move 7 pixels to the right of the screen
            rect.move_ip(7, 0)

        #this will clear the entire screen ( fill it entirely with black )
        # - this is needed to get rid of any of the images that were previously on the screen
        # - after this code is run, we can write images onto the screen
        gameDisplay.fill((0, 0, 0))

#--------------------------------------- Spawns -----------------------------------------------#

        # will spawn a star ( if the spawn chance is greater then a random number )
        # maximum amount of stars spawned is 10
        if(starSpawnChance > random.random() and len(stars) < 10):
            starSpawn()

        # will spawn an enmey ( if the spawn chance is greater then a random number )
        # maximum amount of enemies spawned is 20
        if(enemySpawnChance >= random.random() and len(enemies) < 20):
            enemySpawn()

#--------------------------------------- Bullet Movement -----------------------------------------------#

        #for every bullet in the bullets list
        for bullet in bullets:
            #move the bullet up
            bullet.move()
            #draw the bullet
            pygame.draw.rect(gameDisplay,(0, 250, 0), bullet.rect)
            #if the bullet goes past the top of the screen
            if(bullet.rect.top < 0):
                #remove the bullet from its friends and family
                bullets.remove(bullet)
                #kill the bullet with no witnesses
                del bullet
                #move on and ask no questions
                continue

        # for every bullet in the enemybullets list
        for eBullet in enemybullets:
            #move the bullet down
            eBullet.move()
            #draw the bullet
            pygame.draw.rect(gameDisplay,(255, 0, 0), eBullet.rect)
            #if the bullet moves past the bottom of the screen
            if(eBullet.rect.top > 600):
                #rip the bulllet out of the list
                enemybullets.remove(eBullet)
                #take the bullet out back and kill it from memory
                del eBullet
                #move on
                continue
#--------------------------------------- Player Collision -----------------------------------------------#
            #if the bullet intersects with the player
            if(eBullet.rect.left < rect.left+35 and eBullet.rect.left+5 > rect.left and eBullet.rect.top < rect.top+35 and eBullet.rect.top > rect.top):
                #subtract from the players health
                health -= 1
                #create a temporary text that says - <3
                temprect = wasHurtTextRender.get_rect().move(rect.left, rect.top)
                #insert that text into the hurtText list
                hurtText.append(temprect)

                #take the bullet out of the list
                enemybullets.remove(eBullet)
                #remove the bullet from memory
                del eBullet
                #go on to the next bullet
                continue


        #for every enemy in the list of enemies
        for enemy in enemies:
            #continued is a variable used to tell whether you should continue the loop
            continued = False
            #this is going to check if the enemy has collided with any of the currently active bullets
            #for every bullet in the bullets list
            for bullet in bullets:
                #if the bullet intersects the enemy

#--------------------------------------- Enemy Collision -----------------------------------------------#
                if(bullet.rect.left < enemy.rect.left+35 and bullet.rect.left+5 > enemy.rect.left and bullet.rect.top < enemy.rect.top+35 and bullet.rect.top > enemy.rect.top):
                    #increase the spawn chance of the new enemies
                    enemySpawnChance += 0.002
                    #spawn a new text that says +10
                    temprect = killedEnemy.get_rect().move(enemy.rect.left, enemy.rect.top)
                    #add that to the points list so that it can move out of the screen
                    points.append(temprect)
                    #find the bullet and take it out of the bullets list
                    bullets.remove(bullet)
                    #kill the bullet from memory
                    del bullet
                    #add to the score because you just killed the enemy
                    scoreVal += 10
                    #re-render the text with the updated score
                    score = largeText.render('Score: '+str(scoreVal), True, (255, 255, 255))
                    #now actually remove the enemy from the list
                    enemies.remove(enemy)
                    #kill the enemy
                    del enemy
                    #set the continued bool set outside of this loop to true because we have to continue on to the next enemy
                    continued = True
                    #break out of the bullet loop
                    break
            #if continued is true just move on to the next enemy
            if(continued):
                continue

            #move the enemy
            enemy.step()
            #draw the enemy
            gameDisplay.blit(badGuy, (enemy.rect.left, enemy.rect.top))

        # (when the enemy dies will spawn a point)
        # this loop will move the points up and out of the screen
        # for every point in the points list
        for point in points:
            # move the points up
            point.move_ip(0, -3)
            #draw the point on the screen
            gameDisplay.blit(killedEnemy, point)
            #if the point is out of the top of the screen
            if(point.top < 0):
                #remove the point from the points list
                points.remove(point)
                #destroy the point from memory
                del point
                #move on to the next point
                continue

        # kinda the same thing as the points LOOP
        # this loop will move the hurt text that spawns if the player is hit with an enemy bullet
        #for every text in the hurtText list
        for text in hurtText:
            # move the text up
            text.move_ip(0, -3)
            # draw the text on the screen
            gameDisplay.blit(wasHurtTextRender, text)
            #if the text is out of the screen
            if(text.top < 0):
                #remove the text from the hurtText list
                hurtText.remove(text)
                #remove the text from memory
                del text
                #move onto the next text in hurtText
                continue

        #for each start in the stars list
        for star in stars:
            #move the star down
            star.move()
            #if the star is off the bottom of the screen
            if(star.rect.top > 600):
                #put it back to the top of the screen
                star.rect.move_ip(0, -620)

            #draw the star on the screen
            pygame.draw.rect(gameDisplay,(255, 255, 255), star.rect)

        #draw the highscore onto the screen
        gameDisplay.blit(highScore, (textrect.left, textrect.top+40))
        #draw the score onto the screen
        gameDisplay.blit(score, textrect)

        #there is probably a better way to do this but I was lazy
        #if the players health is > 0 draw the last heart image onto the screen
        if health > 0:
            gameDisplay.blit(heartImg, (30, 15))
        #if the player has no health then display none of the hearts and kill the player
        else:
            #dead keeps the game loop running
            #once dead = true the death screen will appear on the next frame
            dead = True
            print("Player Died")
        #if health is > 1 then the 2nd heart will be drawn onto the screen
        if health > 1:
            gameDisplay.blit(heartImg, (70, 15))
        #if the health is > 2 then the 3rd heart will be drawn onto the screen
        if health > 2:
            gameDisplay.blit(heartImg, (110, 15))

        # if the highscore is < then current score
        #update the highscore with the current score
        if highScoreVal < scoreVal:
            highScoreVal = scoreVal
            highScore = medText.render('High Score: ' + str(highScoreVal), True, (255, 255, 255))
            gameDisplay.blit(highScore, (textrect.left, textrect.top+40))


        #pygame.draw.rect(gameDisplay, (0, 0, 0), rect)

        #draw the player spaceship onto the screen
        gameDisplay.blit(spaceShip, (rect.left, rect.top))
        #update the display
        pygame.display.update()
        #update the time
        clock.tick(40)
    #if the player is dead
    else:

        global death

        global move

        #for every current event
        for event in events:
            # if the player quits quit the game
            if event.type == pygame.QUIT:
                    crashed = True

            # if the player presses a button the game will reset
            if event.type == pygame.KEYDOWN:
                #resetting all the values the gameloop uses
                health = 3
                enemybullets = []
                bullets = []
                stars = []
                enemies = []
                points = []
                hurtText = []
                rect.move(400, 525)


                if highScoreVal < scoreVal:
                    highScoreVal = scoreVal
                    highScore = medText.render('High Score: '+ str(highScoreVal), True, (255, 255, 255))

                scoreVal = 0
                score = largeText.render('Score: '+str(scoreVal), True, (255, 255, 255))

                enemySpawnChance = 0.01
                moveLeft = False
                moveRight = False

                #Reset Game
                dead = False
        print move
        if move != 0:
            #resetting all the values the gameloop uses
            health = 3
            enemybullets = []
            bullets = []
            stars = []
            enemies = []
            points = []
            hurtText = []
            rect.move(400, 525)


            if highScoreVal < scoreVal:
                highScoreVal = scoreVal
                highScore = medText.render('High Score: '+ str(highScoreVal), True, (255, 255, 255))

            scoreVal = 0
            score = largeText.render('Score: '+str(scoreVal), True, (255, 255, 255))

            enemySpawnChance = 0.01
            moveLeft = False
            moveRight = False

            #Reset Game
            dead = False
        #clears the screen
        gameDisplay.fill((0, 0, 0))

        #updates highscore
        if highScoreVal < scoreVal:
            highScoreVal = scoreVal
            highScore = medText.render('High Score: '+ str(highScoreVal), True, (255, 255, 255))

        #draws score to screen
        gameDisplay.blit(score, textrect)
        #draws highscore to screen
        gameDisplay.blit(highScore, (textrect.left, textrect.top+40))

        #draws "you lost" to screen
        lost_rect = youLost.get_rect()
        lost_rect = lost_rect.move(315, 250)
        gameDisplay.blit(youLost, lost_rect)
        #draws "to try again press any button" to screen
        gameDisplay.blit(tryAgain, tryAgain.get_rect().move(175, 350))
        #updates display
        pygame.display.update()

#whent the game loop ends these kill the window
pygame.display.quit()
pygame.quit()
exit()
t1.join()
