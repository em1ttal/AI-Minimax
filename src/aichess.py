#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:22:03 2022

@author: ignasi
"""
import copy
import math

import chess
import board
import numpy as np
import sys
import queue
from typing import List
import time
import random


RawStateType = List[List[List[int]]]

from itertools import permutations


class Aichess():
    """
    A class to represent the game of chess.

    ...

    Attributes:
    -----------
    chess : Chess
        represents the chess game

    Methods:
    --------
    startGame(pos:stup) -> None
        Promotes a pawn that has reached the other side to another, or the same, piece

    """

    def __init__(self, TA, myinit=True):

        if myinit:
            self.chess = chess.Chess(TA, True)
        else:
            self.chess = chess.Chess([], False)

        self.listNextStates = []
        self.listVisitedStates = []
        self.listVisitedSituations = {}
        self.pathToTarget = []
        self.currentStateW = self.chess.boardSim.currentStateW;
        self.depthMax = 8;
        self.checkMate = False

    def copyState(self, state):
        
        copyState = []
        for piece in state:
            copyState.append(piece.copy())
        return copyState
        
    def isVisitedSituation(self, color, mystate):
        
        if (len(self.listVisitedSituations) > 0):
            perm_state = list(permutations(mystate))

            isVisited = False
            for j in range(len(perm_state)):

                for k in range(len(self.listVisitedSituations)):
                    if self.isSameState(list(perm_state[j]), self.listVisitedSituations.__getitem__(k)[1]) and color == \
                            self.listVisitedSituations.__getitem__(k)[0]:
                        isVisited = True

            return isVisited
        else:
            return False


    def getCurrentStateW(self):

        return self.myCurrentStateW

    def getListNextStatesW(self, myState):
        self.chess.boardSim.getListNextStatesW(myState)
        self.listNextStates = self.chess.boardSim.listNextStates.copy()

        return self.listNextStates

    def getListNextStatesB(self, myState):
        self.chess.boardSim.getListNextStatesB(myState)
        self.listNextStates = self.chess.boardSim.listNextStates.copy()

        return self.listNextStates

    def isSameState(self, a, b):

        isSameState1 = True
        # a and b are lists
        for k in range(len(a)):

            if a[k] not in b:
                isSameState1 = False

        isSameState2 = True
        # a and b are lists
        for k in range(len(b)):

            if b[k] not in a:
                isSameState2 = False

        isSameState = isSameState1 and isSameState2
        return isSameState

    def isVisited(self, mystate):

        if (len(self.listVisitedStates) > 0):
            perm_state = list(permutations(mystate))

            isVisited = False
            for j in range(len(perm_state)):

                for k in range(len(self.listVisitedStates)):

                    if self.isSameState(list(perm_state[j]), self.listVisitedStates[k]):
                        isVisited = True

            return isVisited
        else:
            return False

    def isWatchedBk(self, currentState):

        self.newBoardSim(currentState)

        bkPosition = self.getPieceState(currentState, 12)[0:2]
        wkState = self.getPieceState(currentState, 6)
        wrState = self.getPieceState(currentState, 2)

        # Si les negres maten el rei blanc, no és una configuració correcta
        if wkState == None:
            return False
        # Mirem les possibles posicions del rei blanc i mirem si en alguna pot "matar" al rei negre
        for wkPosition in self.getNextPositions(wkState):
            if bkPosition == wkPosition:
                # Tindríem un checkMate
                return True
        if wrState != None:
            # Mirem les possibles posicions de la torre blanca i mirem si en alguna pot "matar" al rei negre
            for wrPosition in self.getNextPositions(wrState):
                if bkPosition == wrPosition:
                    return True
        return False
        


    def isWatchedWk(self, currentState):
        self.newBoardSim(currentState)

        wkPosition = self.getPieceState(currentState, 6)[0:2]
        bkState = self.getPieceState(currentState, 12)
        brState = self.getPieceState(currentState, 8)

        # If whites kill the black king , it is not a correct configuration
        if bkState == None:
            return False
        # We check all possible positions for the black king, and chck if in any of them it may kill the white king
        for bkPosition in self.getNextPositions(bkState):
            if wkPosition == bkPosition:
                # That would be checkMate
                return True
        if brState != None:
            # We check the possible positions of the black tower, and we chck if in any o them it may killt he white king
            for brPosition in self.getNextPositions(brState):
                if wkPosition == brPosition:
                    return True

        return False



    def newBoardSim(self, listStates):
        # We create a  new boardSim
        TA = np.zeros((8, 8))
        for state in listStates:
            TA[state[0]][state[1]] = state[2]

        self.chess.newBoardSim(TA)

    def getPieceState(self, state, piece):
        pieceState = None
        for i in state:
            if i[2] == piece:
                pieceState = i
                break
        return pieceState

    def getCurrentState(self):
        listStates = []
        for i in self.chess.board.currentStateW:
            listStates.append(i)
        for j in self.chess.board.currentStateB:
            listStates.append(j)
        return listStates

    def getNextPositions(self, state):
        # Given a state, we check the next possible states
        # From these, we return a list with position, i.e., [row, column]
        if state == None:
            return None
        if state[2] > 6:
            nextStates = self.getListNextStatesB([state])
        else:
            nextStates = self.getListNextStatesW([state])
        nextPositions = []
        for i in nextStates:
            nextPositions.append(i[0][0:2])
        return nextPositions

    def getWhiteState(self, currentState):
        whiteState = []
        wkState = self.getPieceState(currentState, 6)
        whiteState.append(wkState)
        wrState = self.getPieceState(currentState, 2)
        if wrState != None:
            whiteState.append(wrState)
        return whiteState

    def getBlackState(self, currentState):
        blackState = []
        bkState = self.getPieceState(currentState, 12)
        blackState.append(bkState)
        brState = self.getPieceState(currentState, 8)
        if brState != None:
            blackState.append(brState)
        return blackState

    def getMovement(self, state, nextState):
        # Given a state and a successor state, return the postiion of the piece that has been moved in both states
        pieceState = None
        pieceNextState = None
        for piece in state:
            if piece not in nextState:
                movedPiece = piece[2]
                pieceNext = self.getPieceState(nextState, movedPiece)
                if pieceNext != None:
                    pieceState = piece
                    pieceNextState = pieceNext
                    break

        return [pieceState, pieceNextState]

    def heuristica(self, currentState, color):
        #In this method, we calculate the heuristics for both the whites and black ones
        #The value calculated here is for the whites, 
        # but finally from everything, as a function of the color parameter, we multiply the result by -1
        value = 0

        bkState = self.getPieceState(currentState, 12)
        wkState = self.getPieceState(currentState, 6)
        wrState = self.getPieceState(currentState, 2)
        brState = self.getPieceState(currentState, 8)

        filaBk = bkState[0]
        columnaBk = bkState[1]
        filaWk = wkState[0]
        columnaWk = wkState[1]

        if wrState != None:
            filaWr = wrState[0]
            columnaWr = wrState[1]
        if brState != None:
            filaBr = brState[0]
            columnaBr = brState[1]

        # We check if they killed the black tower
        if brState == None:
            value += 50
            fila = abs(filaBk - filaWk)
            columna = abs(columnaWk - columnaBk)
            distReis = min(fila, columna) + abs(fila - columna)
            if distReis >= 3 and wrState != None:
                filaR = abs(filaBk - filaWr)
                columnaR = abs(columnaWr - columnaBk)
                value += (min(filaR, columnaR) + abs(filaR - columnaR))/10
            # If we are white white, the closer our king from the oponent, the better
            # we substract 7 to the distance between the two kings, since the max distance they can be at in a board is 7 moves
            value += (7 - distReis)
            # If they black king is against a wall, we prioritize him to be at a corner, precisely to corner him
            if bkState[0] == 0 or bkState[0] == 7 or bkState[1] == 0 or bkState[1] == 7:
                value += (abs(filaBk - 3.5) + abs(columnaBk - 3.5)) * 10
            #If not, we will only prioritize that he approahces the wall, to be able to approach the check mate
            else:
                value += (max(abs(filaBk - 3.5), abs(columnaBk - 3.5))) * 10

        # They killed the black tower. Within this method, we consider the same conditions than in the previous condition
        # Within this method we consider the same conditions than in the previous section, but now with reversed values.
        if wrState == None:
            value += -50
            fila = abs(filaBk - filaWk)
            columna = abs(columnaWk - columnaBk)
            distReis = min(fila, columna) + abs(fila - columna)

            if distReis >= 3 and brState != None:
                filaR = abs(filaWk - filaBr)
                columnaR = abs(columnaBr - columnaWk)
                value -= (min(filaR, columnaR) + abs(filaR - columnaR)) / 10
            # If we are white, the close we have our king from the oponent, the better
            # If we substract 7 to the distance between both kings, as this is the max distance they can be at in a chess board
            value += (-7 + distReis)

            if wkState[0] == 0 or wkState[0] == 7 or wkState[1] == 0 or wkState[1] == 7:
                value -= (abs(filaWk - 3.5) + abs(columnaWk - 3.5)) * 10
            else:
                value -= (max(abs(filaWk - 3.5), abs(columnaWk - 3.5))) * 10

        # We are checking blacks
        if self.isWatchedBk(currentState):
            value += 20

        # We are checking whites
        if self.isWatchedWk(currentState):
            value += -20

        # If black, values are negative, otherwise positive
        if not color:
            value = (-1) * value

        return value


    def is_checkmate(self, current_state, color):
        self.newBoardSim(current_state)
        if color:
            wk_pos = self.getPieceState(current_state, 6)
            self.chess.boardSim.getListNextStatesW([wk_pos])
            wk_moves = self.chess.boardSim.listNextStates.copy()
            for move in wk_moves:
                self.newBoardSim(current_state)
                self.chess.moveSim(wk_pos, move[0], False)
                if not self.isWatchedWk(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB): return False
            return True
        bk_pos = self.getPieceState(current_state, 12)
        self.chess.boardSim.getListNextStatesB([bk_pos])
        bk_moves = self.chess.boardSim.listNextStates.copy()
        for move in bk_moves:
            self.newBoardSim(current_state)
            self.chess.moveSim(bk_pos, move[0], False)
            if not self.isWatchedBk(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB): return False
        return True

    def max_rec(self, current_state, depth, turn):
        self.newBoardSim(current_state)
        # If we are at the max depth, or if we have a checkmate, we return the heuristic value
        # Checkmate checked for both players
        if depth == 0 or self.is_checkmate(current_state, True) or self.is_checkmate(current_state, False):
            # We return the heuristic value for the
            return [None, self.heuristica(current_state, turn)]

        max_val = -np.inf
        best_move = None
        # We get the next states
        self.newBoardSim(current_state)
        if turn: next_states = [self.getMovement(current_state, x) for x in self.getListNextStatesW(current_state)]
        else: next_states = [self.getMovement(current_state, x) for x in self.getListNextStatesB(current_state)]

        for pos_move in next_states:
            self.newBoardSim(current_state)
            self.chess.moveSim(pos_move[0], pos_move[1], False)
            # If illegal move, we skip it
            if turn and self.isWatchedWk(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB): continue
            if not turn and self.isWatchedBk(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB): continue

            x, val = self.min_rec(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB, depth - 1,  turn)

            if val > max_val:
                max_val = val
                best_move = pos_move

        if best_move == None: return [None, self.heuristica(current_state, True)]
        return [best_move, max_val]

    def min_rec(self, current_state, depth, turn):
        self.newBoardSim(current_state)
        # If we are at the max depth, or if we have a checkmate, we return the heuristic value
        # Checkmate checked for both players
        if depth == 0 or self.is_checkmate(current_state, True) or self.is_checkmate(current_state, False):
            # We return the heuristic value for the
            return [None, self.heuristica(current_state, turn)]

        min_val = np.inf
        best_move = None
        # We get the next states
        self.newBoardSim(current_state)
        if turn: next_states = [self.getMovement(current_state, x) for x in self.getListNextStatesB(current_state)]
        else: next_states = [self.getMovement(current_state, x) for x in self.getListNextStatesW(current_state)]

        for pos_move in next_states:
            self.newBoardSim(current_state)
            self.chess.moveSim(pos_move[0], pos_move[1], False)
            # If illegal move, we skip it
            if turn and self.isWatchedBk(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB): continue
            if not turn and self.isWatchedWk(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB): continue

            x, val = self.max_rec(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB, depth - 1, turn)

            if val < min_val:
                min_val = val
                best_move = pos_move

        if best_move == None: return [None, self.heuristica(current_state, True)]
        return [best_move, min_val]

    def minimaxGame(self, depthWhite, depthBlack):
        
        currentState = self.getCurrentState()        
        # Your code here
        turn = True
        num_moves = 0
        # Maximizing player here is the player making the move
        while not self.is_checkmate(currentState, True) and not self.is_checkmate(currentState, False):
            if turn:
                next_move_w = self.max_rec(currentState, depthWhite, turn)
                self.chess.move(*next_move_w[0])
            else:
                next_move_b = self.max_rec(currentState, depthBlack, turn)
                self.chess.move(*next_move_b[0])

            turn = not turn
            num_moves += 1
            currentState = self.chess.board.currentStateW + self.chess.board.currentStateB
            self.chess.board.print_board()

            if num_moves == 100 or len(currentState) == 2:
                print("Draw")
                break

        print(num_moves)
        

    def ab_max_rec(self, current_state, depth, turn, alpha=-np.inf, beta=np.inf):
        self.newBoardSim(current_state)
        # If we are at the max depth, or if we have a checkmate, we return the heuristic value
        # Checkmate checked for both players
        if depth == 0 or self.is_checkmate(current_state, True) or self.is_checkmate(current_state, False):
            # We return the heuristic value for the
            return [None, self.heuristica(current_state, turn)]

        max_val = -np.inf
        best_move = None
        # We get the next states
        self.newBoardSim(current_state)
        if turn: next_states = [self.getMovement(current_state, x) for x in self.getListNextStatesW(current_state)]
        else: next_states = [self.getMovement(current_state, x) for x in self.getListNextStatesB(current_state)]
        # Randomize the order of the next states, may improve performance
        random.shuffle(next_states)

        for pos_move in next_states:
            self.newBoardSim(current_state)
            self.chess.moveSim(pos_move[0], pos_move[1], False)
            # If illegal move, we skip it
            if turn and self.isWatchedWk(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB): continue
            if not turn and self.isWatchedBk(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB): continue

            x, val = self.ab_min_rec(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB, depth - 1,  turn, beta, alpha)

            if val > max_val:
                max_val = val
                best_move = pos_move

            if val > alpha:
                alpha = val
                if alpha >= beta:
                    #print("pruning")
                    break

        if best_move == None: return [None, self.heuristica(current_state, True)]
        return [best_move, max_val]

    def ab_min_rec(self, current_state, depth, turn, alpha=-np.inf, beta=np.inf):
        self.newBoardSim(current_state)
        # If we are at the max depth, or if we have a checkmate, we return the heuristic value
        # Checkmate checked for both players
        if depth == 0 or self.is_checkmate(current_state, True) or self.is_checkmate(current_state, False):
            # We return the heuristic value for the
            return [None, self.heuristica(current_state, turn)]

        min_val = np.inf
        best_move = None
        # We get the next states
        self.newBoardSim(current_state)
        if turn: next_states = [self.getMovement(current_state, x) for x in self.getListNextStatesB(current_state)]
        else: next_states = [self.getMovement(current_state, x) for x in self.getListNextStatesW(current_state)]
        # Randomize the order of the next states, may improve performance
        random.shuffle(next_states)

        for pos_move in next_states:
            self.newBoardSim(current_state)
            self.chess.moveSim(pos_move[0], pos_move[1], False)
            # If illegal move, we skip it
            if turn and self.isWatchedBk(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB): continue
            if not turn and self.isWatchedWk(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB): continue

            x, val = self.ab_max_rec(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB, depth - 1, turn, beta, alpha)

            if val < min_val:
                min_val = val
                best_move = pos_move

            if beta > val:
                beta = val
                if beta <= alpha:
                    #print("pruning")
                    break

        if best_move == None: return [None, self.heuristica(current_state, True)]
        return [best_move, min_val]

    def alphaBetaPoda(self, depthWhite, depthBlack):

        currentState = self.getCurrentState()
        # Your code here
        turn = True
        num_moves = 0
        # Maximizing player here is the player making the move
        while not self.is_checkmate(currentState, True) and not self.is_checkmate(currentState, False):
            if turn:
                next_move_w = self.ab_max_rec(currentState, depthWhite, turn)
                # Code used for question 3
                #next_move_w = self.max_rec(currentState, depthWhite, turn)
                self.chess.move(*next_move_w[0])
            else:
                next_move_b = self.ab_max_rec(currentState, depthBlack, turn)
                self.chess.move(*next_move_b[0])

            turn = not turn
            num_moves += 1
            currentState = self.chess.board.currentStateW + self.chess.board.currentStateB
            self.chess.board.print_board()

            if num_moves == 100 or len(currentState) == 2:
                print("Draw")
                break


    def ex_chance_node(self, current_state, depth, turn):
        if depth % 2 == 0:
            move, values = self.ex_min_rec(current_state, depth - 1, turn)
            return [move, self.calculateValue(values)]
        else:
            move, values = self.ex_max_rec(current_state, depth - 1, turn)
            return [move, self.calculateValue(values)]

    def ex_max_rec(self, current_state, depth, turn):
        self.newBoardSim(current_state)
        # If we are at the max depth, or if we have a checkmate, we return the heuristic value
        # Checkmate checked for both players
        if depth == 0 or self.is_checkmate(current_state, True) or self.is_checkmate(current_state, False):
            # We return the heuristic value for the
            return [None, self.heuristica(current_state, turn)]

        max_val = -np.inf
        best_move = None
        # We get the next states
        self.newBoardSim(current_state)
        if turn: next_states = [self.getMovement(current_state, x) for x in self.getListNextStatesW(current_state)]
        else: next_states = [self.getMovement(current_state, x) for x in self.getListNextStatesB(current_state)]

        values = []
        for pos_move in next_states:
            self.newBoardSim(current_state)
            self.chess.moveSim(pos_move[0], pos_move[1], False)
            # If illegal move, we skip it
            if turn and self.isWatchedWk(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB): continue
            if not turn and self.isWatchedBk(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB): continue

            x, val = self.ex_chance_node(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB, depth, turn)
            values.append(val)
            if val > max_val:
                max_val = val
                best_move = pos_move

        if best_move == None: return [None, self.heuristica(current_state, True)]
        return [best_move, values]

    def ex_min_rec(self, current_state, depth, turn):
        self.newBoardSim(current_state)
        # If we are at the max depth, or if we have a checkmate, we return the heuristic value
        # Checkmate checked for both players
        if depth == 0 or self.is_checkmate(current_state, True) or self.is_checkmate(current_state, False):
            # We return the heuristic value for the
            return [None, self.heuristica(current_state, turn)]

        min_val = np.inf
        best_move = None
        # We get the next states
        self.newBoardSim(current_state)
        if turn: next_states = [self.getMovement(current_state, x) for x in self.getListNextStatesB(current_state)]
        else: next_states = [self.getMovement(current_state, x) for x in self.getListNextStatesW(current_state)]
        values = []
        for pos_move in next_states:
            self.newBoardSim(current_state)
            self.chess.moveSim(pos_move[0], pos_move[1], False)
            # If illegal move, we skip it
            if turn and self.isWatchedBk(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB): continue
            if not turn and self.isWatchedWk(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB): continue

            x, val = self.ex_chance_node(self.chess.boardSim.currentStateW + self.chess.boardSim.currentStateB, depth, turn)
            values.append(val)
            if val < min_val:
                min_val = val
                best_move = pos_move

        if best_move == None: return [None, self.heuristica(current_state, True)]
        return [best_move, values]

    def expectimax(self, depthWhite, depthBlack):

        currentState = self.getCurrentState()
        # Your code here
        turn = True
        num_moves = 0
        # Maximizing player here is the player making the move
        while not self.is_checkmate(currentState, True) and not self.is_checkmate(currentState, False):
            if turn:
                next_move_w = self.ex_max_rec(currentState, depthWhite, turn)
                self.chess.move(*next_move_w[0])
            else:
                next_move_b = self.ex_max_rec(currentState, depthBlack, turn)
                self.chess.move(*next_move_b[0])

            turn = not turn
            num_moves += 1
            currentState = self.chess.board.currentStateW + self.chess.board.currentStateB
            self.chess.board.print_board()

            if num_moves == 100 or len(currentState) == 2:
                print("Draw")
                break
        
        

    def mitjana(self, values):
        sum = 0
        N = len(values)
        for i in range(N):
            sum += values[i]

        return sum / N

    def desviacio(self, values, mitjana):
        sum = 0
        N = len(values)

        for i in range(N):
            sum += pow(values[i] - mitjana, 2)

        return pow(sum / N, 1 / 2)

    def calculateValue(self, values):
        
        if len(values) == 0:
            return 0
        mitjana = self.mitjana(values)
        desviacio = self.desviacio(values, mitjana)
        # If deviation is 0, we cannot standardize values, since they are all equal, thus probability willbe equiprobable
        if desviacio == 0:
            # We return another value
            return values[0]

        esperanca = 0
        sum = 0
        N = len(values)
        for i in range(N):
            #Normalize value, with mean and deviation - zcore
            normalizedValues = (values[i] - mitjana) / desviacio
            # make the values positive with function e^(-x), in which x is the standardized value
            positiveValue = pow(1 / math.e, normalizedValues)
            # Here we calculate the expected value, which in the end will be expected value/sum            
            # Our positiveValue/sum represent the probabilities for each value
            # The larger this value, the more likely
            esperanca += positiveValue * values[i]
            sum += positiveValue

        return esperanca / sum
     

if __name__ == "__main__":
    #   if len(sys.argv) < 2:
    #       sys.exit(usage())

    # intiialize board
    TA = np.zeros((8, 8))

    #Configuració inicial del taulell
    TA[7][0] = 2
    TA[7][4] = 6
    TA[0][7] = 8
    TA[0][4] = 12

    # initialise board
    print("stating AI chess... ")
    aichess = Aichess(TA, True)

    print("printing board")
    aichess.chess.boardSim.print_board()

  # Run exercise 1
    #start_time = time.time()
    #aichess.minimaxGame(3, 4)
    #print(f"--- {time.time() - start_time:.2f} seconds ---")
  # Add code to save results and continue with other exercises

  # Run exercise 2, remove comments below, and comment exercise 1
    start_time = time.time()
    aichess.alphaBetaPoda(3, 4)
    print(f"--- {time.time() - start_time:.2f} seconds ---")

