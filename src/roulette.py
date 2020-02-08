import argparse
from bets import *
from collections import defaultdict
import game_setup as gs
import matplotlib.pyplot as plt
import numpy as np
import pprint
import strategies as strat


def find_max_nonzero_bin(histo, bins):
    max_nonzero_idx = 0
    for idx, val in enumerate(histo):
        if val != 0:
            max_nonzero_idx = idx

    return bins[max_nonzero_idx]


class RouletteSim(object):

    def __init__(self, max_num_spins: int,
                 min_bet: int,
                 game_type: str,
                 strategy: strat.RouletteStrategy,
                 plot_results: bool):
        self.max_num_spins = max_num_spins
        self.min_bet = min_bet
        self.game_type = game_type
        self.strategy = strategy
        self.plot_results = plot_results

    def play(self, freq=None, redblack=None, runs=None):

        if self.game_type == 'French':
            wheel = gs.french
        elif self.game_type == 'American':
            wheel = gs.american
        else:
            raise Exception(f'Unsupported game type: {self.game_type}')

        wheel = np.array(wheel)
        game_results_idx = np.random.randint(0, len(wheel), self.max_num_spins)
        game_results = wheel[game_results_idx]

        running_total, history = self.strategy.apply(game_results)
        self.strategy.analyze_history(history,
                                      freq=freq,
                                      redblack=redblack,
                                      runs=runs)
        if self.plot_results:
            self.strategy.plot_history(history)
        return running_total, history


def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", type=str, help="Roulette type",
                        choices=gs.GAME_TYPES, default=gs.GAME_TYPES[0])
    parser.add_argument("-n", "--num_spins", type=int, help="Number of spins", default=100)
    parser.add_argument("-g", "--num_games", type=int, help="Number of games", default=1)
    parser.add_argument("-i", "--minimum_bet", type=int,
                        help="Minimum bet allowed", default=5)
    parser.add_argument("-s", "--strategy", type=str, choices=strat.STRATEGIES,
                        help="Name of the strategy to employ", default=strat.STRATEGIES[0])
    parser.add_argument("--plot_each_game", type=int,
                        help="plot each game result", default=1)
    parser.add_argument("--plot_game_results", type=int,
                        help="plot overall game results", default=1)
    args = parser.parse_args()

    factory = strat.RouletteStrategyFactory(args.minimum_bet)
    strategy = factory.get(args.strategy)

    game_totals = []
    game_histories = []
    freq = defaultdict(int)
    redblack = defaultdict(int)
    runs = defaultdict(list)
    for x in range(args.num_games):
        sim = RouletteSim(max_num_spins=args.num_spins,
                          min_bet=args.minimum_bet,
                          game_type=args.type,
                          strategy=strategy,
                          plot_results=args.plot_each_game==1)
        running_total, game_history = sim.play(freq=freq,
                                               redblack=redblack,
                                               runs=runs)
        game_totals.append(running_total)
        game_histories.append(game_history)

    print(freq)
    print(redblack)
    win_run_histo, _ = np.histogram(runs['win'], bins=100, range=(1, args.num_spins))
    loss_run_histo, _ = np.histogram(runs['loss'], bins=100, range=(1, args.num_spins))
    print(win_run_histo)
    print(loss_run_histo)
    bins = range(1, args.num_spins + 1)
    max_win_streak = find_max_nonzero_bin(win_run_histo, bins)
    max_loss_streak = find_max_nonzero_bin(loss_run_histo, bins)
    max_streak = max(max_loss_streak, max_win_streak)
    print(max_streak)


    fig, ax = plt.subplots(2, 1)
    ax[0].bar(bins, win_run_histo, align='center', label='wins')
    ax[0].set_xlim(1, max_streak)
    ax[0].legend(loc="upper left")
    ax[1].bar(bins, loss_run_histo, align='center', label='losses')
    ax[1].set_xlim(1, max_streak)
    ax[1].legend(loc="upper left")
    plt.show()

    print(f'Game stats: mean: {np.mean(game_totals)}, '
          f'min: {np.min(game_totals)}, '
          f'max: {np.max(game_totals)}, '
          f'std: {np.std(game_totals)}, '
          f'game sum: {np.sum(game_totals)}')

    if args.plot_game_results == 1:
        x = range(len(game_totals))
        plt.plot(x, game_totals, '-r', label='game_totals')
        plt.legend(loc="upper left")
        plt.show()


if __name__ == '__main__':
    main()
