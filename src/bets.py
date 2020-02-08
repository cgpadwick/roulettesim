from game_setup import *

available_bets = {
    '0': {
        'winningSpaces': [0],
        'payout': (35, 1),
        'type': 'any'},
    '00': {
        'winningSpaces': ['00'],
        'payout': (35, 1),
        'type': 'any'},
    'Straight up': {
        'winningSpaces': list(range(0, 37)),
        'payout': (35, 1),
        'type': 'pickone'},
    'Row': {
        'winningSpaces': [0, '00'],
        'payout': (17, 1),
        'type': 'any'},
    'Top line or Basket': {
        'winningSpaces': [0, '00', 1, 2, 3],
        'payout': (5, 1),
        'type': 'any'},
    '1st column': {
        'winningSpaces': [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
        'payout': (2, 1),
        'type': 'any'},
    '2nd column': {
        'winningSpaces': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
        'payout': (2, 1),
        'type': 'any'},
    '3rd column': {
        'winningSpaces': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
        'payout': (2, 1),
        'type': 'any'},
    '1st dozen': {
        'winningSpaces': list(range(1, 13)),
        'payout': (2, 1),
        'type': 'any'},
    '2nd dozen': {
        'winningSpaces': list(range(13, 25)),
        'payout': (2, 1),
        'type': 'any'},
    '3rd dozen': {
        'winningSpaces': list(range(25, 37)),
        'payout': (2, 1),
        'type': 'any'},
    'Odd': {
        'winningSpaces': [item for item in range(1, 37) if item % 2],
        'payout': (1, 1),
        'type': 'any'},
    'Even': {
        'winningSpaces': [item for item in range(1, 37) if not item % 2],
        'payout': (1, 1),
        'type': 'any'},
    'Red': {
        'winningSpaces': list(red),
        'payout': (1, 1),
        'type': 'any'},
    'Black': {
        'winningSpaces': list(black),
        'payout': (1, 1),
        'type': 'any'},
    '1 to 18': {
        'winningSpaces': list(range(1, 19)),
        'payout': (1, 1),
        'type': 'any'},
    '19 to 36': {
        'winningSpaces': list(range(19, 37)),
        'payout': (1, 1),
        'type': 'any'},
    '13 to 18': {
        'winningSpaces': list(range(13, 19)),
        'payout': (5, 1),
        'type': 'any'},
    '16 to 21': {
        'winningSpaces': list(range(16, 22)),
        'payout': (5, 1),
        'type': 'any'},
    '19 to 24': {
        'winningSpaces': list(range(19, 25)),
        'payout': (5, 1),
        'type': 'any'},
    '22 to 27': {
        'winningSpaces': list(range(22, 28)),
        'payout': (5, 1),
        'type': 'any'},
    '25 to 30': {
        'winningSpaces': list(range(25, 31)),
        'payout': (5, 1),
        'type': 'any'},
    '28 to 33': {
        'winningSpaces': list(range(28, 34)),
        'payout': (5, 1),
        'type': 'any'},
    '31 to 36': {
        'winningSpaces': list(range(31, 37)),
        'payout': (5, 1),
        'type': 'any'},
}
