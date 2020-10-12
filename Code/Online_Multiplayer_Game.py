import pygame
import socket
from player import Player
from network import Network

width = 500
height = 500
framerate = 60

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0

def redrawWindow(player1, player2):
    # window has been declared at the highest level
    window.fill((255,255,255))
    player1.draw(window)
    player2.update()
    player2.draw(window)
    pygame.display.update()

def main():
    run = True
    
    clock = pygame.time.Clock()

    client_network = Network()
    player1 = client_network.get_position()
    while run:
        clock.tick(framerate)   
        player2 = client_network.send(player1)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        player1.move()
        redrawWindow(player1, player2)    
main()