# -*- coding: utf-8 -*-

import emoji
import sys
import random

#this global variable is necessary so a player cannot re-enter the same position twice within the same game
already_seen_position = ''

def who_goes_first():
    """Randomly determines if the human or computer goes first. """
    if random.randint(0,1) == 0:
        return 'X'
    else:
        return 'O'

def play_again():
    """ Asks the human if they would like to play another round of tic-tac-toe"""
    print(emoji.emojize("Would you like to play again? (Yes or no) :cherries: ",
                        use_aliases=True))
    input = raw_input().lower()
    if input.startswith('y'):
        return True
    return False

def get_move():
    """Gets the human player's input, including some error-handling. """
    while True:
        move = raw_input("Please enter a move (from 1-9)> ")
        if move.isdigit() is False:
            print(emoji.emojize("Please input only digits :hibiscus:", use_aliases=True))
        elif len(move) != 1:
            print(emoji.emojize('Please only enter one digit. :exclamation: ',
                                use_aliases=True))
        elif move in already_seen_position:
            print(emoji.emojize("That position on the board has already been taken, please guess another position :crescent_moon:", use_aliases=True))
        else:
            return move

def setup_board():
  """Sets up an empty board. '_' is the equivalent to an empty space. """

  return [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]

def is_board_full(board):
  """If board is full, return True. Otherwise, return False.

  >>> is_board_full([['_', '_', '_'], ['X', '_', 'O'], ['_', '_', '_']])
  False

  >>> is_board_full([['X', 'O', '_'], ['X', 'O', 'X'], ['X', 'O', 'X']])
  False

  >>> is_board_full([['X', 'O', 'X'], ['X', 'X', 'O'], ['O', 'O', 'O']])
  True
  """
  for row in board:
      for coli in range(3):
          if row[coli] == '_':
              return False

  return True

def computer_ai(board, player):
  """
  Computer algorithm:
  - Check to see if a corner is open. If so, take it.
  - Check to see if center is open. If so, take it.
  - Take any of the middle-side spaces if open.

  Player is 'X' or 'O'

  Mutates the board in-place.
  Returns position (1-9)

  >>> board = [['X', 'O', 'X'], ['X', 'X', 'O'], ['O', 'O', '_']]
  >>> computer_ai(board, 'X')
  9

  >>> board
  [['X', 'O', 'X'], ['X', 'X', 'O'], ['O', 'O', 'X']]
  """
 #checks top-left corner; if that space is free, take it
  if board[0][0] == '_':
      board[0][0] = player
      return 1
 #checks top-right corner; if that space is free, take it
  elif board[0][2] == '_':
      board[0][2] = player
      return 3
 #checks bottom-left corner; if that space is free, take it
  elif board[2][0] == '_':
      board[2][0] = player
      return 7
 #checks bottom-right corner; if that space is free, take it
  elif board[2][2] == '_':
      board[2][2] = player
      return 9
 #checks center; if that space is free, take it
  elif board[1][1] == '_':
      board[1][1] = player
      return 5
 #moves on one of the sides; if that space is free, take it
  for rowi in range(3):
    for coli in range(3):
      if board[rowi][coli] == '_':
          board[rowi][coli] = player
          board_placement = rowi * 3 + coli + 1
          return board_placement

  raise Exception("Nope, no more empty spaces.")

def find_winner(board):
  """"Given board, determine if winner. Return 'X', 'O', or None if no winner.

  >>> print find_winner([['_', '_', '_'], ['X', '_', 'O'], ['_', '_', '_']])
  None

  >>> find_winner([['X', '_', '_'], ['X', '_', 'O'], ['X', '_', '_']])
  'X'

  >>> find_winner([['X', 'O', 'X'], ['O', 'O', 'X'], ['O', 'X', 'X']])
  'X'

  >>> find_winner([['X', '_', 'O'], ['X', 'O', 'O'], ['O', '_', '_']])
  'O'
  """
  # Check for win in each row
  for rowi in range(3):
      if board[rowi][0] != '_' and board[rowi][0] == board[rowi][1] == board[rowi][2]:
          return board[rowi][0]

  # Check for win in each col
  for coli in range(3):
      if board[0][coli] != '_' and board[0][coli] == board[1][coli] == board[2][coli]:
          return board[0][coli]

  # Check for \ diagonal
  if board[0][0] != '_' and board[0][0] == board[1][1] == board[2][2]:
      return board[0][0]

  # Check for / diagonal
  if board[2][0] != '_' and board[2][0] == board[1][1] == board[0][2]:
      return board[2][0]

def print_board(board):
  """Given a board[col][row], print it.

  >>> print_board([['_', '_', '_'], ['X', '_', 'O'], ['_', '_', '_']])
  _ _ _
  X _ O
  _ _ _
  """

  for row in board:
      for cell in row:
          print cell,
      print


def make_move(board, position, player):
  """Play into position 1-9.

  position = 1-9 (top-left, top-middle, top-right ... bottom-right)
  player = 'X' or 'O'

  Updates board.

  >>> board = [['X', '_', 'O'], ['X', 'O', 'O'], ['O', '_', '_']]

  >>> make_move(board, 2, 'O')
  >>> board
  [['X', 'O', 'O'], ['X', 'O', 'O'], ['O', '_', '_']]

  >>> make_move(board, 9, 'X')
  >>> board
  [['X', 'O', 'O'], ['X', 'O', 'O'], ['O', '_', 'X']]
  """

  coli, rowi = divmod(position - 1, 3)

  board[coli][rowi] = player

def main_loop():
  """This loop contains the overarching tic-tac-toe game logic.
  
  The human is Player X and the computer is Player O.
  
  Loop:
  - Show the board
  - Randomly choose whether the computer or human goes first
  - If it's the human's turn, prompt for a position (1-9) and make their move
  - If it's the computer's turn, the computer follows an algorithm to make any legal move
  - If there's a winner and/or the board is full, exit this round """

  winner = None
  full = False
  global already_seen_position
  board = setup_board()
  current_player = who_goes_first()

  while not winner and not is_board_full(board):
      print
      print_board(board)
      print
      if current_player == 'X':
          print(emoji.emojize("It's your turn, please enter a digit :blue_heart:", use_aliases=True))
          move = get_move()
          already_seen_position += move
          position = int(move)
          make_move(board, position, 'X')
          current_player = 'O'
      else:
          print(emoji.emojize("It's the computer's turn, please wait...:purple_heart:", use_aliases=True))
          position = computer_ai(board, 'O')
          already_seen_position += str(position)
          print(emoji.emojize("The computer :computer: , Player :o: , played in position %s" % position, use_aliases=True))
          current_player = 'X'

      winner = find_winner(board)
      if winner:
          print
          print_board(board)
          print
          print(emoji.emojize(":tada:Congratulations to Player %s:sparkles: :raised_hands: ", use_aliases=True)) % winner
  if not winner and is_board_full(board):
      print(emoji.emojize("There's no winner. It's a tie :musical_note:", use_aliases=True))

def tic_tac_toe_game():
      """
      - Ask the player if they would like to play again
      - If the player would like to play again, this resets the global variable already_seen_position. Otherwise, the program exists.
      """
      while True:
          print(emoji.emojize("Welcome to a :snake: Pythonic :snake: tic-tac-toe game! \nLet's begin, shall we?", use_aliases=True))
          print(emoji.emojize("Please wait while the first player is being randomly generated :four_leaf_clover:", use_aliases=True))

          main_loop()

          restart = play_again()

          if restart:
              global already_seen_position
              already_seen_position = '' #resets seen positions global variable
          if not restart:
              print(emoji.emojize("Goodbye! Have a wonderful day :sunny:", use_aliases=True))
              sys.exit()

if __name__ == "__main__":
  import sys

  if len(sys.argv) > 1 and sys.argv[1] == '--test':
      import doctest

      if doctest.testmod().failed == 0:
          print "\nTests passed! Hooray!\n"
  else:
    tic_tac_toe_game()
