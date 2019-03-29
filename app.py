import os
import time
import random
from numpy import *


#
# classe principal
#
class Game:

    #
    # variaveis
    #
    board           = list(range(1,10))
    emptyBoard      = board[:]
    validFields     = []
    listCPU         = []
    listPlayer      = []
    symbols         = ['O','X']
    turn            = 0

    #
    # Construtor da classe
    #
    def __init__(self):
        self.clear()
        self.putSymbol(1, 'X')
        self.listCPU.insert(0, 1)
        self.drawField()



    def reset(self):
        self.board           = []
        self.emptyBoard      = []
        self.validFields     = []
        self.listCPU         = []
        self.listPlayer      = []

        self.board           = list(range(1,10))
        self.emptyBoard      = self.board[:]

        self.clear()
        self.putSymbol(1, 'X')
        self.listCPU.insert(0, 1)
        self.drawField()
        self.initTurn()

    #
    # Mensagem simples
    #
    def message(self, msg):
        #self.clear()
        print(msg)
        time.sleep(1.2)
        #self.clear()


    #
    # Mensagem com input
    #
    def messageInput(self, msg):
        rtn = input(msg)
        self.clear()
        return rtn


    #
    # Limpa a tela
    #
    def clear(self):
        os.system( 'cls' )


    #
    # Desenha o campo
    #
    def drawField(self):
        self.clear()
        self.draw()


    #
    # Transforma o vetor de posições em uma matriz
    #
    def draw(self):
        #self.clear()
        self.field = reshape(self.board,(3,3))
        print('---------------------')
        for self.cel in self.field:
            print('')
            print(*self.cel, sep="    |    ")

        print('---------------------')


    #
    # Movimento do jogador
    #
    def movePlayer(self):
        while True:
            position = int(self.messageInput('Digite a posição: '))
            if ((position in self.emptyBoard) and (position in self.validFields)):
                self.putSymbol(position, 'O' )
                self.listPlayer.append( position )
                self.listPlayer.sort()
                break

            else:
                self.message('Posição inválida. tente novamente.')
                self.draw()


    #
    # Movimento da máquina
    #
    def moveCpu(self):
        positionCPU = self.IA()
        self.putSymbol(positionCPU, 'X')
        self.listCPU.append( positionCPU )
        self.listCPU.sort()
        self.drawField()
        


    #
    # Insere o simbolo de 'O' ou 'X' conforme o jogador
    #
    def putSymbol(self, position, symbol):
        positionBoard = position - 1
        #print(self.board)
        self.board[positionBoard] = symbol
        #print(self.board)
        self.validFields = self.validPositions()




    #
    # Verifica se a posição é valida
    #
    def validPositions(self):
        currentboard = self.board.copy()
        for removeMoves in self.symbols:
            while removeMoves in currentboard:
                currentboard.remove(removeMoves)
        return currentboard


    #
    # Verifica vitória
    #
    def victoryConditions(self, board):
        listPlay = []
        boardInX = reshape(board,(3,3))
        for c in boardInX:
            listPlay.append(list(c))

        boardInY = reshape(board,(3,3)).swapaxes(0,1)
        for c in boardInY:
            listPlay.append(list(c))

        oddValue = board[0::2]
        oddAux = oddValue[:]
        oddAux.pop(0)
        oddAux.reverse()
        oddAux.pop(0)
        oddAux.reverse()
        listPlay.append(oddAux)

        oddAux = oddValue[:]
        oddAux.pop(1)
        oddAux.reverse()
        oddAux.pop(1)
        oddAux.reverse()
        listPlay.append(oddAux)

        return listPlay


    def playConditions(self):
        listPlay = []
        boardInX = reshape(self.emptyBoard,(3,3))
        for c in boardInX:
            row = list(c)
            for r in row:
                for i in row:
                    if (i != r) and (i > r):
                        us = [r,i]
                        us.sort()
                        listPlay.append(us)

        boardInY = reshape(self.emptyBoard,(3,3)).swapaxes(0,1)
        for c in boardInY:
            row = list(c)
            for r in row:
                for i in row:
                    if (i != r) and (i > r):
                        us = [r,i]
                        us.sort()
                        listPlay.append(us)


        oddValue = self.emptyBoard[0::2]

        oddAux = oddValue[:]
        oddAux.pop(0)
        oddAux.reverse()
        oddAux.pop(0)
        oddAux.reverse()
        for r in oddAux:
            for i in oddAux:
                if (i != r) and (i > r):
                    us = [r,i]
                    us.sort()
                    listPlay.append(us)

        #listPlay.append(oddAux)

        oddAux = oddValue[:]
        oddAux.pop(1)
        oddAux.reverse()
        oddAux.pop(1)
        oddAux.reverse()
        for r in oddAux:
            for i in oddAux:
                if (i != r) and (i > r):
                    us = [r,i]
                    us.sort()
                    listPlay.append(us)

        #listPlay.append(oddAux)

        listPlay.sort()

        return listPlay


    #
    # Calcula o produto cartesiano
    #
    def cartesianProduct(self, listProduct):
        listPlay = []
        for r in listProduct:
            for i in listProduct:
                if (i != r) and (i > r):
                    us = [r,i]
                    listPlay.append(us)
                    listPlay.sort()

        return listPlay

    #
    # IA
    #
    def IA(self):
        rtn = 0
        possibilities = [1,3,7,9]
        play1 = possibilities[0::3] #[1,9]
        play2 = possibilities[1:3] #[3,7]
        play = list(set(possibilities).difference(self.listPlayer).difference(self.listCPU))


        currentPlayCPU = len(self.listCPU)
        #currentPlayPlayer = len(self.listPlayer)

        playConditions = self.playConditions()
        victoryConditions = self.victoryConditions(self.emptyBoard)


        #
        # Primeira jogada
        #
        if currentPlayCPU == 0:
            rtn = random.choice(possibilities)


        #
        # Segunda jogada
        #
        if currentPlayCPU == 1:
            playCPU = self.listCPU[0]
            playPlayer = self.listPlayer[0]
            aux = []

            if self.listPlayer[0] == 5:
                if playCPU in play1:
                    aux = play1[:]
                    aux.remove(playCPU)

                if playCPU in play2:
                    aux = play2[:]
                    aux.remove(playCPU)
                rtn = aux[0]

            elif self.listPlayer[0] not in play1 and self.listCPU[0] in play1:
                aux = play1[:]
                aux.remove(playCPU)
                rtn = aux[0]

            elif self.listPlayer[0] not in play2 and self.listCPU[0] in play2:
                aux = play1[:]
                aux.remove(playCPU)
                rtn = aux[0]

            else:
                rtn = random.choice(play)


        #
        # Terceira jogada
        #
        if currentPlayCPU == 2:
            #
            # verifica se tem como vencer
            #
            for row in playConditions:
                if row == self.listCPU:
                    #print('verifica se tem como vencer')
                    for conditions in victoryConditions:
                        safePlay = conditions[:]
                        play = list(set(safePlay).difference(row))
                        #print(play)
                        if len(play) == 1 and play[0] not in self.listPlayer:
                            rtn = play[0]


            #
            # verifica se o jogador tem como vencer
            #
            if rtn == 0:
                for row in playConditions:
                    if row == self.listPlayer:
                        #print('verifica se o jogador tem como vencer')
                        for conditions in victoryConditions:
                            safePlay = conditions[:]
                            play = list(set(safePlay).difference(row))
                            #print(play)
                            if len(play) == 1 and play[0] not in self.listCPU:
                                rtn = play[0]


            #
            # Se não vencer, monta a estratégia
            #
            if rtn == 0:
                play = list(set(possibilities).difference(self.listCPU).difference(self.listPlayer))
                if len(play) == 1:
                    rtn = play[0]


        #
        # Quarta jogada
        #
        if currentPlayCPU == 3:
            #
            # verifica se tem como vencer
            #
            print('quarta jogada')
            cartesianListCPU = self.cartesianProduct(self.listCPU)
            for rowCPU in cartesianListCPU:
                for row in playConditions:
                    if rowCPU == row:
                        for conditions in victoryConditions:
                            safePlay = conditions[:]
                            play = list(set(safePlay).difference(row))
                            if len(play) == 1 and play[0] not in self.listPlayer:
                                print(play[0])
                                rtn = play[0]


            #
            # verifica se o jogador tem como vencer
            #
            if rtn == 0:
                cartesianListPlayer = self.cartesianProduct(self.listPlayer)
                for rowPlayer in cartesianListPlayer:
                    for row in playConditions:
                        if rowPlayer == row:
                            for conditions in victoryConditions:
                                safePlay = conditions[:]
                                play = list(set(safePlay).difference(row))
                                if len(play) == 1 and play[0] not in self.listCPU:
                                    rtn = play[0]


            #
            # Caso ninguém vença, faz uma jogada aleatória
            #
            if rtn == 0:
                rtn = random.choice(self.validFields)



        #
        # Quinta jogada
        #
        if currentPlayCPU == 4:
            print('# Quinta jogada')
            rtn = random.choice(self.validFields)


        #
        # final da função
        #
        return rtn


    #
    # Verifica a vitória
    #
    def checkVitory(self):
        victory = False
        condition = []
        victoryConditions = self.victoryConditions(self.emptyBoard)

        #symbols
        for symb in self.symbols:
            condition = []
            for position, value in enumerate(self.board):
                if value == symb:
                    condition.append(position+1)
                else:
                    condition.append(0)

            playsForVictory = self.victoryConditions(list(condition))

            for rowVictory in victoryConditions:
                for rowPlays in playsForVictory:
                    if rowVictory == rowPlays:
                        victory = True
                        break

        return victory


    def addTurn(self):
        self.turn = self.turn + 1

    def getTurn(self):
        return self.turn

    def initTurn(self):
        self.turn = 0


#
# chamada do jogo
#
x = Game()
while True:
    x.addTurn()
    x.movePlayer()
    x.moveCpu()
    if x.checkVitory():
        rtn = x.messageInput('Não foi dessa vez. Deseja jogar novamente?(S/N)')
        if rtn.upper() == 'S':
            x.reset()
            continue
        else:
            break

    if x.getTurn() == 4:
        rtn = x.messageInput('Empatamos. Deseja jogar novamente?(S/N)')
        if rtn.upper() == 'S':
            x.reset()
            continue
        else:
            break