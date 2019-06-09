from Q_learning import *
import pickle
import matplotlib.pyplot as plt


def train():
    board = chess.Board()
    numberOfGames = 0
    agent = Agent(gameObject=board)
    counters = []
    counter = 0
    while numberOfGames < 100:
        a , pathCounter  = agent.train()
        if a:
            numberOfGames += a
            counters.append(pathCounter)
        counter+=1
        print(counter)
        print(board)
        if not (counter % 50):
            pickle.dump(agent.Q_Matrix, open('Q_Matrix.p', "wb"))

    plt.plot(counters)
    plt.title("Number of Paths for a game")
    plt.xlabel("n_th game")
    plt.ylabel("Number of Paths")
    plt.savefig('stat.png')




def main():
   train()


if __name__ == '__main__':
    main()
