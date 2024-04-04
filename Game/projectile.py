import pygame
pygame.init()

window = pygame.display.set_mode((750,650))
pygame.display.set_caption("New Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')
red = pygame.image.load('red.png')
red_l = pygame.image.load('red_left.png')
town = pygame.image.load('town.jpeg')

town2 = pygame.transform.scale(town, (int(town.get_width() * 3), int(town.get_height() * 3)))

run = True

class enemy():
    
    def __init__(self, x, y) :
        
        self.x = x
        self.y = y
        self.vel = 3
        self.walkcount = 1
        self.dir = 1            #direction
        self.height = 64
        self.width = 64
        self.hitbox = (self.x+15, self.y+10, 30, 50)
        
        
    def draw(self, window):

        hitbox = (self.x+15, self.y+10, 30, 50)

        if(self.x > 600 ):
            self.dir = -1
        elif(self.x < 10):
            self.dir = 1

        if(self.dir > 0 and self.x < 600 ):
            self.x += self.vel
            pygame.draw.rect(window, (0,255,0), hitbox, 2)
            window.blit(walkRight[self.walkcount%9], (self.x, self.y))
            self.walkcount += 1
        else:
            self.x -= self.vel
            window.blit(walkLeft[self.walkcount%9], (self.x, self.y))
            pygame.draw.rect(window, (0,255,0), hitbox, 2)
            self.walkcount += 1

    def hit(self):

        print('Hit')

class projectile():

    def __init__(self, x, y, radius, color, facing):

        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 9*facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class player():

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.left = False
        self.right = False
        self.jumpcount = 15
        self.isJump = False

    def display(self, window):
        # if walkcount + 1 >= 27:
        #     walkcount = 0
        hitbox = (self.x, self.y, 50, 60)
        if self.left:
            window.blit(red_l, (self.x,self.y))
            pygame.draw.rect(window, (255,0,0), hitbox, 2)
            # window.blit(walkLeft[walkcount//9], (x,y))
            # walkcount += 1
    
        elif self.right:
            window.blit(red, (self.x,self.y))
            pygame.draw.rect(window, (255,0,0), hitbox, 2)
            # window.blit(walkRight[walkcount // 9], (x,y))
            # walkcount += 1

        else:
            window.blit(red, (self.x,self.y))
            pygame.draw.rect(window, (255,0,0), hitbox, 2)


def showbackground ():
    global walkcount
    window.fill((102,255,178))
    # new_town = pygame.surface((750, 750))
    window.blit(town2, (0,10))

    rishi.display(window) 
    vader.draw(window)

    for bullet in bullets:
        bullet.draw(window)        

    pygame.display.update()

rishi = player(600, 500, 64, 64)
bullets = []
vader = enemy(400, 400)

#main loop
while run:

    pygame.time.delay(15)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    for bullet in bullets:



        if bullet.x < 900 and bullet.x > 0:
            bullet.x += bullet.vel
            
            if(bullet.x > vader.x and bullet.x < vader.x+10):
                if(bullet.y < vader.y+10 and bullet.y > vader.y):

                    bullets.pop(bullet.index(bullet))
                    vader.hit()

        else:
            bullets.pop(bullets.index(bullet))
        

    keys = pygame.key.get_pressed()
    # mouse = pygame.MOUSEBUTTONDOWN
    if keys[pygame.K_LCTRL]:

        dir = 1

        if rishi.left:
            dir = -1

        if len(bullets) < 1 :
            bullets.append(projectile(rishi.x + rishi.width, rishi.y+20, 4, (0,0,0), dir))

    if(keys[pygame.K_SPACE]):
        rishi.isJump = True

    if(rishi.isJump):
        
        if(keys[pygame.K_RIGHT] and rishi.x < 700):
            rishi.x += rishi.vel
            rishi.left = False
            rishi.right = True

        elif(keys[pygame.K_LEFT]):
            rishi.x -= rishi.vel
            rishi.left = True
            rishi.right = False
        else:
            rishi.left = False
            rishi.right = False
            rishi.walkcount = 0

        if(rishi.jumpcount >= -15):
            neg = -1
            # print("here")
            
            if(rishi.jumpcount < 0):
                neg = 1

            rishi.y += (rishi.jumpcount**2)*0.1*neg
            rishi.jumpcount -= 1

        else:
            rishi.jumpcount = 15
            rishi.isJump = False

    else:
        if(keys[pygame.K_RIGHT] and rishi.x < 700 ):
            rishi.x += rishi.vel
            rishi.left = False
            rishi.right = True
        if(keys[pygame.K_LEFT]):
            rishi.x -= rishi.vel
            rishi.left = True
            rishi.right = False
        if (keys[pygame.K_UP]):
            rishi.y -= rishi.vel
        if(keys[pygame.K_DOWN]):
            rishi.y += rishi.vel

    if rishi.x >= 750:
        rishi.x = 750

    if rishi.y >= 750:
        rishi.y = 750

    if rishi.x < 0:
        rishi.x = 0

    if rishi.y < 0:
        rishi.y = 0

    showbackground()
