from util import *

def run(board):
    board.initialize_random_tile()
    board.initialize_random_tile()
    print(board)
    while True:
        if board.is_game_over():
            break

        direction = input("Use arrow key: ")
        if direction not in [UP, DOWN, LEFT, RIGHT]:
            continue
        board.move(direction)
        board.initialize_random_tile()
        print(board) 

    if board.game_state == LOSE:
        print("Game over, you lose!")
    elif board.game_state == WIN:
        print("Congrats, you win!")

if __name__ == "__main__":
    n = int(input("Enter a board size: "))
    run(Board(n)) 

