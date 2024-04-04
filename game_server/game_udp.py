
import pygame
import socket
import sys
import time

game_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
game_server.bind(('localhost', 8000))
# game_server.listen(1)

print("Waiting for connection...")

# try:
#     # control_client, client_address = game_server.accept()
#     # print("Connected to:", client_address)
# except KeyboardInterrupt:
#     pygame.quit()
#     sys.exit()

pygame.init()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("First game")

x = 250
y = 250
width = 40
height = 60
vel = 10

run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= vel
    if keys[pygame.K_RIGHT]:
        x += vel
    if keys[pygame.K_UP]:
        y-= vel
    if keys[pygame.K_DOWN]:
        y+= vel
    # 

    try:
        start_time = time.time()
        data, address = game_server.recvfrom(1024)
        end_time = time.time()
        # data = control_client.recv(1)
        # if not data:
        #     break
        print(f"latency :{end_time-start_time}")

        direction = data[0]
        if direction == 0:
            print("Received: Left")
            x -= vel
        elif direction == 1:
            print("Received: Right")
            x += vel
        elif direction == 2:
            print("Received: Up")
            y -= vel
        elif direction == 3:
            print("Received: Down")
            y += vel
        elif direction == 5:
            print("jump")
            # y += vel
        elif direction == 4:
            print("No movement")

        win.fill((0, 0, 0))
        pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
        pygame.display.update()

        response = '1'
        game_server.sendto(response.encode(), address)
    except ConnectionResetError:
        print("Client disconnected.")
        break

# Close the sockets
# control_client.close()
game_server.close()
pygame.quit()
sys.exit()