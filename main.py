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
        # print(counter)
        print(agent.gameObject)
        if not (counter % 50):
            pickle.dump(agent.Q_Matrix, open('Q_Matrix.p', "wb"))

    plt.plot(counters)
    plt.title("Number of Paths for a game")
    plt.xlabel("n_th game")
    plt.ylabel("Number of Paths")
    plt.savefig('stat.png')


def test():
    q_matrix = pickle.load(open('Q_Matrix.p', "rb"))
    board = chess.Board()
    agent = Agent(Q_Matrix=q_matrix, gameObject=board)
    while not agent.gameObject.is_game_over():
        print("Computer's turn ...")
        agent.play()
        print(agent.gameObject)
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
   # train()
    test()

if __name__ == '__main__':
    main()
