class Game:
    def __init__(self, id):
        self.player1Moved = False
        self.player2Moved = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self. ties = 0

    def get_player_move(self, playerID):
        return self.moves[playerID]

    def play(self, playerID, move):
        self.moves[playerID] = move
        if playerID == 0:
            self.player1Moved = True
        else:
            self.player2Moved = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.player1Moved and self.player2Moved

    def winner(self):
                
        player1 = self.moves[0].upper()[0]
        player2 = self.moves[1].upper()[0]

        winner = -1 # tie game

        if player1 == "R" and player2 == "S":
            winner = 0
        elif player1 == "S" and player2 == "R":
            winner = 1
        elif player1 == "P" and player2 == "R":
            winner = 0
        elif player1 == "R" and player2 == "P":
            winner = 1
        elif player1 == "S" and player2 == "P":
            winner = 0
        elif player1 == "P" and player2 == "S":
            winner = 1
            
        return winner

    def resetWent(self):
        self.player1Moved = False
        self.player2Moved = False 
        