import pygame
import socket
import sys
import time


pygame.init()

window = pygame.display.set_mode((750,650))
pygame.display.set_caption("New Game")

walkRight = [pygame.image.load('Game/assets/R1.png'), pygame.image.load('Game/assets/R2.png'), pygame.image.load('Game/assets/R3.png'), pygame.image.load('Game/assets/R4.png'), pygame.image.load('Game/assets/R5.png'), pygame.image.load('Game/assets/R6.png'), pygame.image.load('Game/assets/R7.png'), pygame.image.load('Game/assets/R8.png'), pygame.image.load('Game/assets/R9.png')]
walkLeft = [pygame.image.load('Game/assets/L1.png'), pygame.image.load('Game/assets/L2.png'), pygame.image.load('Game/assets/L3.png'), pygame.image.load('Game/assets/L4.png'), pygame.image.load('Game/assets/L5.png'), pygame.image.load('Game/assets/L6.png'), pygame.image.load('Game/assets/L7.png'), pygame.image.load('Game/assets/L8.png'), pygame.image.load('Game/assets/L9.png')]
bg = pygame.image.load('Game/assets/bg.jpg')
char = pygame.image.load('Game/assets/standing.png')
red = pygame.image.load('Game/assets/red.png')
red_l = pygame.image.load('Game/assets/red_left.png')
town = pygame.image.load('Game/assets/town.jpeg')
# town2 = pygame.transform.scale(town, (500, 500))

town2 = pygame.transform.scale(town, (int(town.get_width() * 3), int(town.get_height() * 3)))



run = True

class player():

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 15
        self.left = False
        self.right = False
        self.jumpcount = 10
        self.isJump = False

    def display(self, window):
        # if walkcount + 1 >= 27:
        #     walkcount = 0

        # else:
            if self.left:
                window.blit(red_l, (self.x,self.y))
            # window.blit(walkLeft[walkcount//9], (x,y))
            # walkcount += 1
    
            elif self.right:
                window.blit(red, (self.x,self.y))
            # window.blit(walkRight[walkcount // 9], (x,y))
            # walkcount += 1

            else:
                window.blit(red, (self.x,self.y))

class projectile():
    def __init__(self, x, y, ) -> None:
        pass

def showbackground ():
    global walkcount
    window.fill((102,255,178))
    # new_town = pygame.surface((750, 750))
    window.blit(town2, (0,10))

    player.display(window) 

    pygame.display.update()

player = player(600, 500, 64, 64)

game_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
game_server.bind(('localhost', 8000))

print("Waiting for connection...")

client_connected = True

while run:

    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # keys = pygame.key.get_pressed()

    # if(keys[pygame.K_SPACE]):
    #     player.isJump = True

    # if(player.isJump):
        
    #     if(keys[pygame.K_RIGHT] and player.x < 700):
    #         player.x += player.vel
    #         player.left = False
    #         player.right = True

    #     elif(keys[pygame.K_LEFT]):
    #         player.x -= player.vel
    #         player.left = True
    #         player.right = False
    #     else:
    #         player.left = False
    #         player.right = False
    #         player.walkcount = 0

    #     if(player.jumpcount >= -15):
    #         neg = -1
    #         # print("here")
            
    #         if(player.jumpcount < 0):
    #             neg = 1

    #         player.y += (player.jumpcount**2)*0.1*neg
    #         player.jumpcount -= 1

    #     else:
    #         player.jumpcount = 15
    #         player.isJump = False

    # else:
    #     if(keys[pygame.K_RIGHT] and player.x < 700 ):
    #         player.x += player.vel
    #         player.left = False
    #         player.right = True
    #     if(keys[pygame.K_LEFT]):
    #         player.x -= player.vel
    #         player.left = True
    #         player.right = False
    #     if (keys[pygame.K_UP]):
    #         player.y -= player.vel
    #     if(keys[pygame.K_DOWN]):
    #         player.y += player.vel

    # if player.x >= 750:
    #     player.x = 750

    # if player.y >= 750:
    #     player.y = 750

    # if player.x < 0:
    #     player.x = 0

    # if player.y < 0:
    #     player.y = 0

    # showbackground()
    
    try:
        start_time = time.time()
        data, address = game_server.recvfrom(1024)
        end_time = time.time()

        print(f"latency :{end_time-start_time}")

        direction = data[0]

        print(direction)

        if direction == 1:
            if player.x < 700:
                player.x += player.vel
                
                player.left = False
                player.right = True
        elif direction == 0:
            player.x -= player.vel
            player.left = True
            player.right = False
        elif direction == 2:
            player.y -= player.vel
        elif direction == 3:
            player.y += player.vel
        elif direction == 5:
            player.isJump = True
        
        if player.isJump:
            if player.jumpcount >= -12:
                neg = 1 if player.jumpcount < 0 else -1
                player.y += (player.jumpcount ** 2) * 0.3 * neg
                player.jumpcount -= 1
            else:
                player.isJump = False
                player.jumpcount = 12

        window.fill((102,255,178)) # Clear the screen
        window.blit(town2, (0,10))
        # Display player
        player.display(window)
        pygame.display.update()

        response = '1'
        game_server.sendto(response.encode(), address)
        client_connected = True


    except ConnectionResetError:
        client_connected = False
        run = False
        if not client_connected:
            # If client was already disconnected, break out of loop
            break
        print("Client disconnected.")

# Close the sockets
# control_client.close()
game_server.close()
pygame.quit()
sys.exit()
