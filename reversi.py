import tkinter
import random
import time
import math

class Reversi:
    def __init__(self):
        self.board = []
        for i in range(8):
            self.board.append([0] * 8)
        self.board[3][3] = 1
        self.board[3][4] = 2
        self.board[4][3] = 2
        self.board[4][4] = 1
        self.turn = 1
        self.black = 2
        self.white = 2
        self.gameOver = False
        self.winner = 0
        self.computer = False
        self.computerTurn = False
        self.computerColor = 2
        self.computerMove = 0
        self.difficulty = 3


    def getTurn(self):
        return self.turn

    def getBlack(self):
        return self.black

    def getWhite(self):
        return self.white

    def getGameOver(self):
        return self.gameOver

    def getWinner(self):
        return self.winner

    def getComputer(self):
        return self.computer

    def getComputerTurn(self):
        return self.computerTurn

    def getComputerColor(self):
        return self.computerColor

    def getComputerMove(self):
        return self.computerMove

    def getDifficulty(self):
        return self.difficulty

    def setComputer(self, computer):
        self.computer = computer

    def setComputerColor(self, computerColor):
        self.computerColor = computerColor

    def setComputerMove(self, computerMove):
        self.computerMove = computerMove

    def setComputerTurn(self, computerTurn):
        self.computerTurn = computerTurn

    def setTurn(self, turn):
        self.turn = turn

    def setBlack(self, black):
        self.black = black

    def setWhite(self, white):
        self.white = white

    def setGameOver(self, gameOver):
        self.gameOver = gameOver

    def setWinner(self, winner):
        self.winner = winner

    def getBoard(self):
        return self.board

    def setBoard(self, board):
        self.board = board

    def getPiece(self, row, col):
        return self.board[row][col]

    def setPiece(self, row, col, piece):
        self.board[row][col] = piece

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty

    

    #resets the board to original state, whenever the restart button is pressed
    def resetBoard(self):
        self.board = []
        for i in range(8):
            self.board.append([0] * 8)
        self.board[3][3] = 1
        self.board[3][4] = 2
        self.board[4][3] = 2
        self.board[4][4] = 1
        self.turn = 1
        self.black = 2
        self.white = 2
        self.gameOver = False
        self.winner = 0
        self.computer = False
        self.computerTurn = False
        self.computerColor = 2
        self.computerMoveAttribute = 0
        self.difficulty = 3

    def getValidMoves(self):
        moves = []
        for row in range(8):
            for col in range(8):
                if self.isValidMove(row, col):
                    moves.append([row, col])
        return moves

    def isValidMove(self, row, col):
        if self.board[row][col] != 0:
            return False
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if self.isValidMoveDirection(row, col, i, j):
                    return True
        return False

    def isValidMoveDirection(self, row, col, rowDirection, colDirection):
        if row + rowDirection < 0 or row + rowDirection > 7 or \
           col + colDirection < 0 or col + colDirection > 7:
            return False
        if self.board[row + rowDirection][col + colDirection] == 0:
            return False
        if self.board[row + rowDirection][col + colDirection] == self.turn:
            return False
        for i in range(2, 8):
            if row + i * rowDirection < 0 or row + i * rowDirection > 7 or \
               col + i * colDirection < 0 or col + i * colDirection > 7:
                return False
            if self.board[row + i * rowDirection][col + i * colDirection] == 0:
                return False
            if self.board[row + i * rowDirection][col + i * colDirection] == self.turn:
                return True
        return False

    def makeMove(self, row, col):
        #first check if the game is over
        if self.isGameOver() == True:
            #display the winner and show score
            self.gameOver = True
            self.winner = self.getWinner()


        self.board[row][col] = self.turn
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if self.isValidMoveDirection(row, col, i, j):
                    self.makeMoveDirection(row, col, i, j)
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1


        #first check if the game is over
        if self.isGameOver() == True:
            #display the winner and show score
            self.gameOver = True
            self.winner = self.getWinner()


    def makeMoveDirection(self, row, col, rowDirection, colDirection):
        for i in range(1, 8):
            if row + i * rowDirection < 0 or row + i * rowDirection > 7 or \
               col + i * colDirection < 0 or col + i * colDirection > 7:
                return
            if self.board[row + i * rowDirection][col + i * colDirection] == 0:
                return
            if self.board[row + i * rowDirection][col + i * colDirection] == self.turn:
                for j in range(1, i):
                    self.board[row + j * rowDirection][col + j * colDirection] = self.turn
                return

    def isGameOver(self):
        if self.black + self.white == 64:
            return True
        for row in range(8):
            for col in range(8):
                if self.isValidMove(row, col):
                    return False
        return True

    def getWinner(self):
        if self.black > self.white:
            return 1
        elif self.black < self.white:
            return 2
        else:
            return 0

    #computer will choose what move to make based on how many pieces it can flip, best move is then assinged to self.computerMoveAttribute

    def computerMoveHueristic(self):
        bestMove = 0
        bestMoveCount = 0
        for row in range(8):
            for col in range(8):
                if self.isValidMove(row, col):
                    count = 0
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i == 0 and j == 0:
                                continue
                            if self.isValidMoveDirection(row, col, i, j):
                                count += self.makeMoveDirectionCount(row, col, i, j)
                    if count > bestMoveCount:
                        bestMoveCount = count
                        bestMove = [row, col]
        self.computerMoveAttribute = bestMove

    def makeMoveDirectionCount(self, row, col, rowDirection, colDirection):
        count = 0
        for i in range(1, 8):
            if row + i * rowDirection < 0 or row + i * rowDirection > 7 or \
               col + i * colDirection < 0 or col + i * colDirection > 7:
                return 0
            if self.board[row + i * rowDirection][col + i * colDirection] == 0:
                return 0
            if self.board[row + i * rowDirection][col + i * colDirection] == self.turn:
                return count
            count += 1

    #use alpha beta pruning function with the minimax algorithm to determine the best move, list that has row and column, for the computer move is then assigned to self.computerMoveAttribute
    def computerMoveAlphaBeta(self):
        bestMove = 0
        bestMoveCount = 0
        for row in range(8):
            for col in range(8):
                if self.isValidMove(row, col):
                    count = 0
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i == 0 and j == 0:
                                continue
                            if self.isValidMoveDirection(row, col, i, j):
                                count += self.makeMoveDirectionCount(row, col, i, j)
                    if count > bestMoveCount:
                        bestMoveCount = count
                        bestMove = [row, col]

        self.computerMoveAttribute = bestMove
    
    def minimax(self, depth, alpha, beta, maximizingPlayer):
        if depth == 0:
            return self.evaluateBoard()
        # implementing minimax 
        if maximizingPlayer:

            maxEval = -999999
            for row in range(8):
                for col in range(8):
                    if self.isValidMove(row, col):
                        self.makeMove(row, col)
                        eval = self.minimax(depth - 1, alpha, beta, False)
                        self.undoMove(row, col)
                        maxEval = max(maxEval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return maxEval

        else:
            minEval = 999999
            for row in range(8):
                for col in range(8):
                    if self.isValidMove(row, col):
                        self.makeMove(row, col)
                        eval = self.minimax(depth - 1, alpha, beta, True)
                        self.undoMove(row, col)
                        minEval = min(minEval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return minEval

    def evaluateBoard(self):
        score = 0
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == 1:
                    score += 1
                elif self.board[row][col] == 2:
                    score -= 1
        return score

    def undoMove(self, row, col):
        self.board[row][col] = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if self.isValidMoveDirection(row, col, i, j):
                    self.makeMoveDirection(row, col, i, j)

        if self.turn == 1:

            self.black -= 1
            self.white += 1
            self.turn = 2

        else:
                
            self.black += 1
            self.white -= 1
            self.turn = 1

    
     
    
class ReversiGUI:
    def __init__(self):
        self.reversi = Reversi()
        self.window = tkinter.Tk()
        self.window.title("Reversi")
        self.window.resizable(width = False, height = False)
        self.window.protocol("WM_DELETE_WINDOW", self.quit)

        self.canvas = tkinter.Canvas(self.window, width = 400, height = 400)
        self.canvas.pack()

        self.canvas2 = tkinter.Canvas(self.window, width = 400, height = 200, bg = "black")
        self.canvas2.pack()

        self.canvas.bind("<Button-1>", self.mouseLeftPressed)
        self.canvas.bind("<Button-3>", self.mouseRightPressed)

        self.drawBoard()
        self.drawPieces()

        self.window.mainloop()

    def quit(self):
        self.window.destroy()

    #count the number of black and white pieces on the board
    def countPieces(self):
        self.reversi.black = 0
        self.reversi.white = 0
        for row in range(8):
            for col in range(8):
                if self.reversi.getPiece(row, col) == 1:
                    self.reversi.black += 1
                elif self.reversi.getPiece(row, col) == 2:
                    self.reversi.white += 1
        return self.reversi.black, self.reversi.white


    def mouseLeftPressed(self, event):

        row = int(event.y / 50)
        col = int(event.x / 50)
        if self.reversi.isValidMove(row, col):
            self.reversi.makeMove(row, col)
            self.drawPieces()
            
            #The player's move should be displayed near instantaneously, but the computer's move should be delayed by 1 second.
            if self.reversi.getComputer() == False:
                if self.reversi.getDifficulty() == 1:
                    self.reversi.turn = 2
                    if self.reversi.getComputer() == False:
                        self.reversi.setComputerTurn(True)
                        moves = self.reversi.getValidMoves()
                        if len(moves) == 0:
                            self.reversi.setComputerTurn(False)
                            return
                        self.reversi.computerMoveAttribute = random.choice(moves)
                        self.reversi.makeMove(self.reversi.computerMoveAttribute[0], self.reversi.computerMoveAttribute[1])
                    self.drawPieces()
                    self.reversi.setComputerTurn(False)
                    self.reversi.turn = 1

                #Computer makes moves based on a hueuristic function
                elif self.reversi.getDifficulty() == 2:
                    self.reversi.turn = 2
                    if self.reversi.getComputer() == False:
                        self.reversi.setComputerTurn(True)
                        moves = self.reversi.getValidMoves()
                        if len(moves) == 0:
                            self.reversi.setComputerTurn(False)
                            return
                        self.reversi.computerMoveHueristic()
                        self.reversi.makeMove(self.reversi.computerMoveAttribute[0], self.reversi.computerMoveAttribute[1])
                    self.drawPieces()
                    self.reversi.setComputerTurn(False)
                    self.reversi.turn = 1

                #Computer makes moves based on alpha beta pruning with minimax algorithm
                elif self.reversi.getDifficulty() == 3:
                    self.reversi.turn = 2
                    if self.reversi.getComputer() == False:
                        self.reversi.setComputerTurn(True)
                        moves = self.reversi.getValidMoves()
                        if len(moves) == 0:
                            self.reversi.setComputerTurn(False)
                            return
                        self.reversi.computerMoveAlphaBeta()
                        self.reversi.makeMove(self.reversi.computerMoveAttribute[0], self.reversi.computerMoveAttribute[1])
                    self.drawPieces()
                    self.reversi.setComputerTurn(False)
                    self.reversi.turn = 1
        
                    

    #if right click, restart the game
    def mouseRightPressed(self, event):
        self.reversi = Reversi()
        self.drawBoard()
        self.drawPieces()
        #clear the text on canvas2
        self.canvas2.delete("all")
        

    def drawBoard(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    color = "#082552"
                else:
                    color = "#0a3578"
                self.canvas.create_rectangle(50 * col, 50 * row,
                                             50 * col + 50, 50 * row + 50,
                                             fill = color, width = 0)


    #display who wins
    def drawPieces(self):
        if self.reversi.gameOver == True:
            if self.countPieces()[0] > self.countPieces()[1]:
                self.canvas2.create_text(200, 150, text = "Black Wins! Player Wins", fill = "white", font = ("Helvetica", 16))
            elif self.countPieces()[0] < self.countPieces()[1]:
                self.canvas2.create_text(200, 150, text = "White Wins! - Computer Wins", fill = "white", font = ("Helvetica", 16))
            else:
                self.canvas2.create_text(200, 150, text = "Tie!", fill = "white", font = ("Helvetica", 30))

        


        self.drawBoard()
        self.drawScore()
        self.drawTurn()

        for row in range(8):
            for col in range(8):
                if self.reversi.getPiece(row, col) == 1:
                    self.canvas.create_oval(50 * col + 5, 50 * row + 5,
                                            50 * col + 45, 50 * row + 45,
                                            fill = "black", width = 0)
                elif self.reversi.getPiece(row, col) == 2:
                    self.canvas.create_oval(50 * col + 5, 50 * row + 5,
                                            50 * col + 45, 50 * row + 45,
                                            fill = "white", width = 0)

        #a visual aid to show where they can place of piece from valid moves
        if self.reversi.getComputer() == False:
            for row in range(8):
                for col in range(8):
                    if self.reversi.isValidMove(row, col):
                        self.canvas.create_oval(50 * col + 15, 50 * row + 15,
                                                50 * col + 35, 50 * row + 35,
                                                fill = "green", width = 0)


    def isGameOver(self):
        self.canvas2.create_rectangle(0, 0, 400, 400, fill = "gray", width = 0)
        self.canvas2.create_text(200, 200, text = "Game Over", font = ("Helvetica", 32), fill = "white")

    #display the winner of the game
    def drawWinner(self):
        self.canvas2.create_rectangle(0, 0, 400, 400, fill = "gray", width = 0)
        if self.reversi.getWinner() == 1:
            self.canvas2.create_text(200, 200, text = "Black Wins! - Player", font = ("Helvetica", 32), fill = "white")
        elif self.reversi.getWinner() == 2:
            self.canvas2.create_text(200, 200, text = "White Wins! - Computer", font = ("Helvetica", 32), fill = "white")
        else:
            self.canvas2.create_text(200, 200, text = "Tie Game!", font = ("Helvetica", 32), fill = "white")

    #function that draws the score of the game
    def drawScore(self):
        self.canvas2.create_rectangle(0, 0, 400, 50, fill = "black", width = 0)
        self.canvas2.create_text(200, 25, text = "Black: %d, White: %d" % (self.countPieces()[0], self.countPieces()[1]), font = ("Helvetica", 14), fill = "white")

    #draw whose turn it is to play the next move
    def drawTurn(self):
        self.canvas2.create_rectangle(0, 50, 400, 100, fill = "black", width = 0)
        if self.reversi.getTurn() == 1:
            self.canvas2.create_text(200, 75, text = "Black's Turn - Your Turn", font = ("Helvetica", 14), fill = "white")
        else:
            self.canvas2.create_text(200, 75, text = "White's Turn - Computer Turn", font = ("Helvetica", 14), fill = "white")


ReversiGUI()

#an algorithm for making a computer move using random choice
class ReversiAI:
    def __init__(self, reversi):
        self.reversi = reversi

    def computerMoveRandom(self):
        moves = self.reversi.getValidMoves()
        if len(moves) == 0:
            return
        move = random.choice(moves)
        self.reversi.makeMove(move[0], move[1])



    