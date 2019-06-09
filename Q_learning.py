#! python3
"""
Author: Long Phan, Nhut Le
Module: Q_learning.py
"""
import chess
import numpy as np
import operator
import copy
class Agent:
    def __init__(self, Q_Matrix = None, lr = 0.1, gamma = 0.9, gameObject = None):

        self.gameObject = gameObject
        self.pathCounter = 0
        # Initializing Q_Matrix: dict{board: a dictionary of actions}, an action is UCI_move:score

        if Q_Matrix is None:
            self.Q_Matrix = {}
        else:
            self.Q_Matrix = Q_Matrix

        # learning rate
        self.lr = lr
        #gamma
        self.gamma = gamma
        self.scoreTable = {
            'None': 0,
            'q' : 9,
            'r' : 5,
            'n' : 3,
            'b' : 3,
            'p' : 1,
            'k' : 1000000
        }

    # # this function for testing,
    def play(self):
        action = self.actionWithMaxQ_ValInState(self.gameObject.fen(),isMutated=False)
        self.gameObject.push_uci(action)

    def getActions(self, state): #return actions in the state
        # if the state doesnt exist, create it.
        if not state in self.Q_Matrix:
            self.Q_Matrix[state] = {}
        return self.Q_Matrix[state]

    def swapSide(self, state):
        boardStateArray1 = state.split(' ')
        boardStateArray1[0] = boardStateArray1[0].swapcase()
        boardStateArray2 = boardStateArray1[0].split('/')
        boardStateArray2.reverse()
        boardStateArray2 = [x[::-1] for x in boardStateArray2]
        boardStateArray1[0] = '/'.join(boardStateArray2) # Piece placement (from White's perspective)
        boardStateArray1[1] = 'w' # Active color. "w" means White moves next, "b" means Black moves next. Always set to "w"
        boardStateArray1[2] = boardStateArray1[2].swapcase() # Castling availability
        uppercases = ''
        lowercases = ''
        for c in boardStateArray1[2]:
            if c.isupper():
                uppercases += c
            else:
                lowercases += c
        boardStateArray1[2] = uppercases + lowercases
        if boardStateArray1[3] != '-': # En passant target square in algebraic notation
            boardStateArray1[3] = self.swapLocation(boardStateArray1[3])
        boardStateArray1 = ' '.join(boardStateArray1)
        return boardStateArray1

    def swapAction(self, uci_str):
        start = uci_str[:2] # get the first 2 characters
        end = uci_str[2:4] # get the 3rd and 4th characters
        promotion = ''
        if len(uci_str) == 5:
            promotion = uci_str[4] # get the 5th character if it is there
        return self.swapLocation(start) + self.swapLocation(end) + promotion

    def swapLocation(self, algebraic_location_str):
        boardSquares = copy.deepcopy(chess.SQUARE_NAMES)
        boardSquares.reverse()
        algebraic_location_str = boardSquares[chess.SQUARE_NAMES.index(algebraic_location_str)]
        return algebraic_location_str

    def getNextStateFrom(self, state, action):
        currentBoard = chess.Board(state)
        currentBoard.push_uci(action)
        nextState = currentBoard.fen()
        return nextState


    def actionWithMaxQ_ValInState(self, state, isMutated): #return action

        newState = copy.deepcopy(state)
        if not self.gameObject.turn:
            newState = self.swapSide(state)

        virtualBoard = chess.Board(newState)
        actions = self.getActions(newState)

        if (not bool(actions)) or isMutated:

            possibleActions = np.array([a for a in virtualBoard.legal_moves], dtype=str)

            randomChoice = np.random.randint(0, len(possibleActions))

            chosenAction = possibleActions[randomChoice]

            # "f2f4" -> "f4"
            piece = virtualBoard.piece_at(chess.SQUARE_NAMES.index(chosenAction[2:4]))

            scoreForAction = self.scoreTable[str(piece)]

            if chosenAction not in actions:
                #initializing
                actions[chosenAction] = scoreForAction
            ## mutating
            else:
                nextState = self.getNextStateFrom(newState, chosenAction)
                self.getActions(nextState)
                nextStateActions = self.Q_Matrix[nextState]
                if bool(nextStateActions):
                    actions[chosenAction] = actions[chosenAction] + self.lr*(scoreForAction + self.gamma*max(nextStateActions.items(), key=operator.itemgetter(1))[1]-actions[chosenAction])
                else:
                    actions[chosenAction] = actions[chosenAction] + self.lr*(scoreForAction-actions[chosenAction])

        else:
            chosenAction = max(actions.items(), key=operator.itemgetter(1))[0]
            piece = virtualBoard.piece_at(chess.SQUARE_NAMES.index(chosenAction[2:4]))
            scoreForAction = self.scoreTable[str(piece)]
            nextState = self.getNextStateFrom(newState, chosenAction)
            self.getActions(nextState)
            nextStateActions = self.Q_Matrix[nextState]
            if bool(nextStateActions):
                actions[chosenAction] = actions[chosenAction] + self.lr*(scoreForAction + self.gamma*max(nextStateActions.items(), key=operator.itemgetter(1))[1]-actions[chosenAction])
            else:
                actions[chosenAction] = actions[chosenAction] + self.lr*(scoreForAction-actions[chosenAction])

        if not self.gameObject.turn:
            chosenAction = self.swapAction(chosenAction)
        return chosenAction

    def train(self):
        # epsilon
        # self.epsilon = epsilon

        currentState = self.gameObject.fen()

        #mutation or not
        isMutated = np.random.randint(0,9) < 3
        action = self.actionWithMaxQ_ValInState(currentState, isMutated=isMutated)

        # if self.gameObject.turn:
        #     print("w")
        # else:
        #     print("b")
        # print(action)
        self.pathCounter +=1
        self.gameObject.push_uci(action)
        if self.gameObject.is_game_over():
            self.gameObject = chess.Board()
            return 1, self.pathCounter

        return 0, self.pathCounter


