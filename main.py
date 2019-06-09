#! python3
"""
Author: Long Phan, Nhut Le
Module: main.py
"""
from Q_learning import *
import pickle
import matplotlib.pyplot as plt

def randomPlayer(board):
    possibleActions = np.array([a for a in board.legal_moves], dtype=str)
    l = len(possibleActions)
    if l == 0:
        return "0000"
    randomChoice = np.random.randint(l)
    chosenAction = possibleActions[randomChoice]
    return chosenAction

def playVSRandom(testAgent):
    board = chess.Board()
    testAgent = Agent(gameObject=board)
    while not testAgent.gameObject.is_game_over():
        testAgent.play()
        testAgent.gameObject.push_uci(randomPlayer(testAgent.gameObject))
    result = testAgent.gameObject.result()
    def convert_to_float(frac_str):
        try:
            return float(frac_str)
        except ValueError:
            return 0.5
    return convert_to_float(result)

def train():
    board = chess.Board()
    numberOfGames = 0
    agent = Agent(gameObject=board)
    counters = []
    oldNumberOfGames = numberOfGames
    numberOfWins = []
    while numberOfGames < 50000:
        a , pathCounter  = agent.train()
        if a:
            numberOfGames += a
            agent.pathCounter = 0

        if ((oldNumberOfGames != numberOfGames) and not (numberOfGames % 100)):
            counters.append(pathCounter)
            numberOfWin = 0
            for i in range(10):
                result = playVSRandom(agent)
                if result == 0:
                    numberOfWin -=1
                if result == 1:
                    numberOfWin +=1

            numberOfWins.append(numberOfWin*40)
            print('Processed numberOfGames: ', numberOfGames)
            pickle.dump(agent.Q_Matrix, open('Q_Matrix.p', "wb"))
            plt.figure(1)
            plt.clf()
            plt.plot(counters)
            plt.title("Number of moves for a game")
            plt.xlabel("(nx100)_th game")
            plt.ylabel("Number of moves")
            plt.savefig('stat.png')

            plt.figure(2)
            plt.clf()
            plt.plot(numberOfWins)
            plt.title("Elo at n_th game")
            plt.xlabel("(nx100)_th game")
            plt.ylabel("Elo")
            plt.savefig('elo.png')
            oldNumberOfGames = numberOfGames

def test():
    q_matrix = pickle.load(open('Q_Matrix.p', "rb"))
    board = chess.Board()
    agent = Agent(Q_Matrix=q_matrix, gameObject=board)
    while not agent.gameObject.is_game_over():
        print()
        print("Computer's turn ...")
        agent.play()
        print(agent.gameObject)
        print()
        print("The player's turn ....")
        move = str(input("Enter move:"))
        possible_moves = np.array([a for a in agent.gameObject.legal_moves], dtype=str)
        while move not in possible_moves:
            move = str(input("The move is not valid, please enter the move again:"))
        agent.gameObject.push_uci(move)
        print(agent.gameObject)
        print()
        print("-------------------------------------")

def main():
   train()
   #  test()

if __name__ == '__main__':
    main()
