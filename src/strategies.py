import bets as bets
from collections import defaultdict
import game_setup as gs
import matplotlib.pyplot as plt
import numpy as np

STRATEGIES = ['Martingale', 'JamesBond']


class RouletteStrategy(object):

    def __init__(self):
        self.history = []

    def place_bets(self, bet_sizes: list, bets: list):
        bets_played = [(bet_size, bet) for bet_size, bet in zip(bet_sizes, bets)]
        return bets_played

    def outcome(self, winning_number: int, bets_played: list):
        total = 0
        for record in bets_played:
            bet_size, bet = record
            if winning_number in bet['winningSpaces']:
                a, b = bet['payout']
                total += bet_size * a / b
            else:
                total -= bet_size
        return total

    def analyze_history(self, history, freq, redblack, runs):
        def win_or_loss(outcome):
            if outcome < 0:
                return 'loss'
            return 'win'

        def red_black_other(winning_number):
            if winning_number in list(gs.red):
                return 'red'
            elif winning_number in list(gs.black):
                return 'black'
            else:
                return 'other'

        outcomes = [rec['outcome'] for rec in history]
        winning_numbers = [rec['winning_number'] for rec in history]

        # Frequency analysis
        for number in winning_numbers:
            freq[number] += 1

        # red/black
        for number in winning_numbers:
            redblack[red_black_other(number)] += 1

        # Consecutive wins/losses
        idx = ctr = 1
        last_outcome = win_or_loss(outcomes[0])
        while idx < len(outcomes):
            this_outcome = win_or_loss(outcomes[idx])
            if this_outcome == last_outcome:
                # Streak continues
                ctr += 1
            else:
                # Streak Broken
                runs[last_outcome].append(ctr)
                ctr = 1
            last_outcome = this_outcome
            idx += 1

    def plot_history(self, history):

        outcomes = [rec['outcome'] for rec in history]
        totals = [rec['running_total'] for rec in history]
        bets_played = [rec['bets_played'] for rec in history]
        bets_placed = []
        for rec in bets_played:
            total_bet = np.sum([bet_size for bet_size, bet in rec])
            bets_placed.append(total_bet)

        x = range(len(outcomes))
        fig, ax = plt.subplots(3, 1)
        ax[0].plot(x, outcomes, '-r', label='outcomes')
        ax[0].legend(loc="upper left")
        ax[1].plot(x, totals, '-b', label='running total')
        ax[1].legend(loc="upper left")
        ax[2].plot(x, bets_placed, '-g', label='bets placed')
        ax[2].legend(loc="upper left")
        plt.show()


class MartingaleStrategy(RouletteStrategy):

    def __init__(self, min_bet: int):
        self.min_bet = min_bet
        self.bets = [bets.available_bets['Red']]
        super(RouletteStrategy, self).__init__()

    def apply(self, results):
        self.history = []
        running_total = 0
        multiplier = 1
        lost_last_play = False
        for winning_number in results:
            if lost_last_play:
                multiplier *= 2
            else:
                multiplier = 1
            bet_sizes = [self.min_bet * multiplier] * len(self.bets)
            bets_played = self.place_bets(bet_sizes, self.bets)
            spin_outcome = self.outcome(winning_number, bets_played)
            running_total += spin_outcome
            lost_last_play = spin_outcome < 0
            self.history.append({'winning_number': winning_number,
                                 'bets_played': bets_played,
                                 'outcome': spin_outcome,
                                 'running_total': running_total})

        return running_total, self.history


class JamesBond(RouletteStrategy):

    def __init__(self, min_bet: int):
        self.min_bet = min_bet
        self.bets = [bets.available_bets['19 to 36'],
                     bets.available_bets['13 to 18'],
                     bets.available_bets['0']]
        super(RouletteStrategy, self).__init__()

    def apply(self, results):
        self.history = []
        running_total = 0
        multiplier = 1
        lost_last_play = False
        for winning_number in results:
            if lost_last_play:
                multiplier *= 2
            else:
                multiplier = 1
            bet_sizes = [140 * multiplier, 50 * multiplier, 10]
            bets_played = self.place_bets(bet_sizes, self.bets)
            spin_outcome = self.outcome(winning_number, bets_played)
            running_total += spin_outcome
            lost_last_play = spin_outcome < 0
            self.history.append({'winning_number': winning_number,
                                 'bets_played': bets_played,
                                 'outcome': spin_outcome,
                                 'running_total': running_total})

        return running_total, self.history


class RouletteStrategyFactory(object):

    def __init__(self, min_bet: int):
        self.min_bet = min_bet

    def get(self, name):

        if name == 'Martingale':
            return MartingaleStrategy(self.min_bet)
        elif name == 'JamesBond':
            return JamesBond(self.min_bet)
        else:
            raise Exception(f'Strategy {name} is not supported')

