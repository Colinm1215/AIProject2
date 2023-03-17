import TicTacToeClass as TTTC


def main():
    size = int(input("size:"))
    ttt = TTTC.TicTacToe(size, size)
    var = TTTC.play_game(ttt, dict(X=TTTC.player(TTTC.alphabeta_search), O=TTTC.player(TTTC.alphabeta_search)), verbose=True).utility


if __name__ == "__main__":
    main()