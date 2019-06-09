#! python3
"""
Author: Long Phan, Nhut Le
Module: main.py
"""
from Q_learning import *
import pickle
import matplotlib.pyplot as plt


def train():
    board = chess.Board()
    numberOfGames = 0
    agent = Agent(gameObject=board)
    counters = []
    oldNumberOfGames = numberOfGames
    while numberOfGames < 10000:
        a , pathCounter  = agent.train()
        if a:
            numberOfGames += a
            counters.append(pathCounter)
            agent.pathCounter = 0

        if ((oldNumberOfGames != numberOfGames) and not (numberOfGames % 100)):
            print('Processed numberOfGames: ', numberOfGames)
            pickle.dump(agent.Q_Matrix, open('Q_Matrix.p', "wb"))
            plt.clf()
            plt.plot(counters)
            plt.title("Number of moves for a game")
            plt.xlabel("n_th game")
            plt.ylabel("Number of moves")
            plt.savefig('stat.png')
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
