import pygame
from network import Network
import pickle
from time import sleep

pygame.font.init()

width = 700
height = 700
screen_center = (width/2, height/2)
window = pygame. display.set_mode((width, height))
pygame.display.set_caption("Client")

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        window.blit(text, (self.x + round(self.width/2 - round(text.get_width()/2)), self.y + round(self.height/2 - round(text.get_height()/2))))

    def click(self, position):
        x1 = position[0]
        y1 = position[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

def redrawWindow(window, game, playerID):
    window.fill((128,128,128))
    if not game.connected():
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for other Player... ", 1, (255, 0, 0), True)
        window.blit(text, (screen_center[0] - text.get_width()/2, screen_center[1] - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0,255,255))
        window.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0,255,255))
        window.blit(text, (380, 200))

        player1Move = game.get_player_move(0)
        player2Move = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(player1Move, 1, (0,0,0))
            text2 = font.render(player2Move, 1, (0,0,0))
        else:
            if game.player1Moved and playerID == 0:
                text1 = font.render(player1Move, 1, (0,0,0))
            elif game.player1Moved:
                text1 = font.render("Locked in", 1, (0,0,0))
            else:
                text1 = font.render("Waiting... ", 1, (0,0,0))

            if game.player2Moved and playerID == 1:
                text2 = font.render(player2Move, 1, (0,0,0))
            elif game.player2Moved:
                text2 = font.render("Locked in", 1, (0,0,0))
            else:
                text2 = font.render("Waiting... ", 1, (0,0,0))
        
        if playerID == 1:
            window.blit(text2, (100, 350))
            window.blit(text1, (400, 350))
        else:
            window.blit(text1, (100, 350))
            window.blit(text2, (400, 350))
    for button in buttons:
        button.draw(window)
    pygame.display.update()



buttons = [Button("Rock", 50, 500, (0,0,0)), Button("Scissors", 250, 500, (255,0,0)), Button("Paper", 450, 500, (0,255,0))]

def main():
    run = True
    clock = pygame.time.Clock()
    connection = Network()
    player = int(connection.get_playerID())
    

    while run:
        clock.tick(60)
        try: 
            game = connection.send("get")
        except:
            run = False
            print("Could not get game from server")
            break
        
        if game.bothWent():
            redrawWindow(window, game, player)
            pygame.time.delay(500)
            try:
                game = connection.send("reset")
            except:
                run = False
                print("Couldn't get game from server")
                break
            
            font = pygame.font.SysFont("comicsans", 90)
            if game.winner() == player:
                text = font.render("You Won!", 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
            else:
                text = font.render("You Lost!", 1, (255,0,0))
            window.blit(text, (width/2 - text.get_width()//2, height/2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                for button in buttons:
                    if button.click(position) and game.connected():
                        if player == 0:
                            if not game.player1Moved:
                                connection.send(button.text)
                        else:
                            if not game.player2Moved:
                                connection.send(button.text)

        redrawWindow(window, game, player)


main()
