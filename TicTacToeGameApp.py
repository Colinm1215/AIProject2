import TicTacToeClass as TTTC


def main():
    player_strats = {
        'm': TTTC.player(TTTC.minimax_search),
        'a': TTTC.player(TTTC.alphabeta_search),
        'r': TTTC.random_player
    }
    game_running = True
    while game_running:
        size = int(input("size:"))
        ttt = TTTC.TicTacToe(size, size)
        player_x = input("Input strategy for X player:")
        player_o = input("Input strategy for O player:")
        TTTC.play_game(ttt, dict(X=player_strats.get(player_x, TTTC.random_player), O=player_strats.get(player_o, TTTC.random_player)), verbose=True).utility
        play_again = ''
        while play_again not in ['y', 'n']:
            play_again = input("Would you like to play again? (y/n):")
        game_running = (True if play_again == 'y' else False)
    print("Thank You for Playing Our Game!")


if __name__ == "__main__":
    main()
